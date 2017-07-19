from flask import Flask,render_template,url_for
from sqlalchemy import create_engine,text
import math
from math import ceil
import customFilter
import sys

reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
engine=create_engine('mysql://root:mysql122500@localhost/mouse_tf_atlas')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tissue/<tissueName>/<int:page>')
def tissue(tissueName,page):
    conn=engine.connect()
    proc=text('call tissue_gene(:t,:p,@repetition,@total)')
    tissueGene=conn.execute(proc,t=tissueName,p=page).fetchall()
    metadata=conn.execute('select @repetition as repetition,@total as total').fetchone()
    conn.close();
    repetitionThead=['First','Second','Third','Fourth','Fifth']

    prev=True
    nex=True
    block=5
    totalPage=int(ceil(metadata['total']/20.0))
    if page==0:
        prev=False
    if page>=totalPage-5:
        nex=False
        block=totalPage-page
    page={'prev':prev,'next':nex,'page':page,'block':block}
    return render_template('tissue.html',tissueName=tissueName,repetitionThead=repetitionThead,tissueGene=tissueGene,metadata=metadata,page=page) 

@app.route('/tf/<geneSymbol>/<isSearch>')
def tf(geneSymbol,isSearch):
    conn=engine.connect()
    geneTissueList,infoList=[],[]
    if isSearch=='1':  
        select=text("select gene_symbol from gene_symbol where gene_symbol like :g")
        geneSymbolList=conn.execute(select,g=geneSymbol+'%').fetchall()
    else:
        geneSymbolList=[{'gene_symbol':geneSymbol}]
    for row in geneSymbolList:
        geneTissue,info=gene_tissue(row['gene_symbol'],conn)
        geneTissueList.append(geneTissue)
        infoList.append(info)
    conn.close()
    return render_template('tf.html',gT_gS_info=zip(geneTissueList,geneSymbolList,infoList))

def gene_tissue(geneSymbol,conn):
    proc=text('call gene_tissue(:g,@count,@fetalTf,@dermTf,@ttmTf,@description)')
    geneTissue=conn.execute(proc,g=geneSymbol).fetchall()
    info=conn.execute('select @count as count,@fetalTf as fetalTf,@dermTf as dermTf,@ttmTf as ttmTf,@description as description').fetchone()
    return geneTissue,info

@app.route('/download')
def download():
    return render_template('download.html')

@app.route('/workflow')
def workflow():
    return render_template('workflow.html')
    
@app.route('/analysis/expression')
def expression():
    return render_template('/analysis/expression.html')

@app.route('/analysis/dbtf')
def dbtf():
    return render_template('/analysis/dbtf.html')

@app.route('/analysis/network')
def network():
    return render_template('/analysis/network.html')

@app.route('/analysis/coexpression')
def coexpression():
    return render_template('/analysis/coexpression.html')

@app.route('/analysis/coexpression/detail')
def coexpressionDetail():
    return render_template('/analysis/coexpression/detail.html')

@app.route('/analysis/interaction')
def interaction():
    return render_template('/analysis/interaction.html')

@app.route('/analysis/interaction/detail')
def interactionDetail():
    return render_template('/analysis/interaction/detail.html')

@app.route('/analysis/ttm')
def ttm():
    return render_template('/analysis/ttm.html')

@app.route('/analysis/ttm/detail')
def ttmDetail():
    return render_template('/analysis/ttm/detail.html')

@app.template_filter('logFot')
def logFot(fot):
    if fot!=0:
        return round(math.log(fot*1e10,10),3);
    else:
        return 0.0

if __name__ == '__main__':
    app.debug=True
    #app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    #env=app.jinja_env
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.run()
