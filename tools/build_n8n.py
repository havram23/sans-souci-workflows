import json
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

ROOT = Path(__file__).resolve().parents[1]


def main():
    catalog = json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))
    (ROOT/'n8n').mkdir(exist_ok=True)
    examples = [{'id':'A-001','company':'Beispiel Studio','private_note':'synthetisch'}, {'id':'a-001','company':'Beispiel Studio','private_note':'doppelter Export'}, {'id':'','company':'','note':'=1+1','amount':-12}]
    for entry in catalog:
        if entry['format'] != 'n8n': continue
        slug = entry['id'].removeprefix('n8n-')
        code = (ROOT/'n8n-src'/f'{slug}.js').read_text(encoding='utf-8')
        def node(name, kind, version, x, parameters):
            return {'id':str(uuid5(NAMESPACE_URL,entry['id']+name)),'name':name,'type':kind,'typeVersion':version,'position':[x,280],'parameters':parameters}
        nodes = [node('Manuell starten','n8n-nodes-base.manualTrigger',1,260,{}),
                 node('Synthetische Beispiele','n8n-nodes-base.code',2,510,{'mode':'runOnceForAllItems','jsCode':'return '+json.dumps([{'json':x} for x in examples],ensure_ascii=False)+';'}),
                 node('Lokal verarbeiten','n8n-nodes-base.code',2,760,{'mode':'runOnceForAllItems','jsCode':code})]
        connections = {nodes[i]['name']:{'main':[[{'node':nodes[i+1]['name'],'type':'main','index':0}]]} for i in (0,1)}
        workflow = {'name':'Sans Souci – '+entry['title'],'nodes':nodes,'connections':connections,'settings':{'executionOrder':'v1'},'active':False,'pinData':{},'tags':[]}
        (ROOT/'n8n'/f"{entry['id']}.json").write_text(json.dumps(workflow,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('4 inaktive n8n-Vorlagen erzeugt.')


if __name__=='__main__':main()
