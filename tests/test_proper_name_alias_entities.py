"""Encoded name aliases must survive CSV parsing and exact source ownership."""
import csv
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT=Path(__file__).resolve().parents[1]/'template/epub_pipeline/common/scripts/translation_unit_pipeline.py'
spec=importlib.util.spec_from_file_location('encoded_name_alias_pipeline',SCRIPT)
pipeline=importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)

class EncodedNameAliasTests(unittest.TestCase):
    def test_legacy_alias_separators_remain_supported(self):
        self.assertEqual(['First','Second','Third'],pipeline.parse_aliases(' First ; Second | Third ;; '))
        self.assertEqual([],pipeline.parse_aliases(' ; | '))

    def test_numeric_references_do_not_split_names(self):
        self.assertEqual(["Maker&#x27;s Guide","Maker&#39;s Guide","Maker&#X27;s Guide"],pipeline.parse_aliases("Maker&#x27;s Guide;Maker&#39;s Guide|Maker&#X27;s Guide"))

    def test_named_references_and_adjacent_delimiters(self):
        self.assertEqual(['A&amp;B','A&apos;B','C'],pipeline.parse_aliases('A&amp;B;A&apos;B|C'))

    def test_encoded_separator_is_source_text_not_alias_separator(self):
        self.assertEqual(['A&#124;B','A&#59;B'],pipeline.parse_aliases('A&#124;B|A&#59;B'))

    def make_fixture(self,root):
        names=[]
        for eid,source,target,aliases in [('guide','Maker’s Guide','《制作者指南》',"Maker&#x27;s Guide"),('person','Maker','制作者','')]:
            row={k:'' for k in pipeline.REQUIRED_NAME_COLUMNS}
            row.update(entity_id=eid,source_name=source,target_name=target,source_aliases=aliases,category='proper_noun',display_policy='3',first_rendering=f'{target}（{source}）',subsequent_rendering=target,status='locked',display_strategy='target_source_then_target',first_occurrence_rule='first_natural_body_only',same_name_disambiguation='controlled isolated fixture',note_required='false')
            names.append(row)
        def write(path,rows,columns):
            with path.open('w',encoding='utf-8',newline='') as f:
                w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(rows)
        write(root/'names.csv',names,list(names[0]))
        contract={'proper_nouns':{'register':'names.csv','occurrence_ledger':'occurrences.csv'}}
        units=[];ledger=[]
        for uid,kind,source,first in [('title','heading',"Maker&#x27;s Guide",False),('body','body','Maker’s Guide',True),('index','raw_html',"<em>Maker&#x27;s Guide</em>",False)]:
            start=source.index('Maker');end=source.index('Guide')+5
            units.append({'unit_id':uid,'unit_type':kind,'source_file':'fixture.md','source_text':source,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'target_state':'translated','target_template':'{{pn:guide}}','target_text':''})
            ledger.append({'occurrence_id':uid,'source_file':'fixture.md','unit_id':uid,'start_offset':str(start),'end_offset':str(end),'source_form':source[start:end],'entity_id':'guide','disambiguation_evidence':'controlled non-body/body roles; complete title owns nested name','is_body_occurrence':'true' if first else 'false','counts_as_first_body_occurrence':'true' if first else 'false','status':'locked'})
        write(root/'occurrences.csv',ledger,list(ledger[0]))
        return names,contract,units

    def test_csv_alias_retains_exact_longest_title_ownership(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);names,contract,units=self.make_fixture(root)
            _,loaded,_=pipeline.load_name_rows(root,contract)
            forms={f for row in loaded for f in pipeline.name_forms(row)[0]}
            source="<em>Maker&#x27;s Guide</em> by Maker"
            self.assertEqual([(4,22,"Maker&#x27;s Guide"),(31,36,'Maker')],pipeline.find_form_occurrences(source,forms))

    def test_heading_and_index_do_not_consume_first_body_rendering(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);_,contract,units=self.make_fixture(root)
            rendered,issues=pipeline.render_target_templates(root,contract,units)
            self.assertEqual([],issues)
            self.assertEqual({'title':'《制作者指南》','body':'《制作者指南》（Maker’s Guide）','index':'《制作者指南》'},rendered)

    def test_encoded_alias_cannot_bypass_csv_marker_rendering(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);_,contract,units=self.make_fixture(root)
            units[1]['target_template']="{{pn:guide}} Maker&#x27;s Guide"
            _,issues=pipeline.render_target_templates(root,contract,units)
            self.assertTrue(any('CSV_ONLY_RENDER_REQUIRED' in x and 'Maker&#x27;s Guide' in x for x in issues),issues)

if __name__=='__main__':unittest.main()
