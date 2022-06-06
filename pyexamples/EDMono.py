
import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),
    
    # Input (event voxels)
    to_input( '../events.png' ),
    to_input( '../events.png', to='(-2.7,0,0)' , name="640x480x15"),
    
    # Header
    to_Conv_BatchNorm_Relu(name='h', s_filer=640, n_filer=32, offset="(0,0,0)", to="(0,0,0)", width=3, height=40, depth=40, caption="header" ),

    # Encoders
    *block_ConvLSTM_Layer( name='e1', botton='h', s_filer=320, n_filer=64, offset="(1.5,0,0)", size=(32,32,3.5), opacity=0.5 ),
    *block_ConvLSTM_Layer( name='e2', botton='clstm_e1', s_filer=160, n_filer=128, offset="(1.5,0,0)", size=(25,25,4.5), opacity=0.5 ),
    *block_ConvLSTM_Layer( name='e3', botton='clstm_e2', s_filer=80,  n_filer=256, offset="(1.5,0,0)", size=(16,16,5.5), opacity=0.5 ),

    # Residuals
    #block-005
    *block_Res(num=2, name='r4', botton='clstm_e3', top='relu_r4', s_filer=80, n_filer=256, offset="(0.5,0,0)", size=(12,12,5.5), opacity=0.5 ),
    *block_Res(num=2, name='r5', botton='relu_r4', top='relu_r5', s_filer=80, n_filer=256, offset="(0.5,0,0)", size=(12,12,5.5), opacity=0.5 ),

    # Decoders
    *block_Decoder( name="b6", botton="relu_r5", top='end_b6', s_filer=80,  n_filer=128, offset="(1.1,0,0)", size=(16,16,5.0), opacity=0.5 ),
    to_skip( of='clstm_e3', to='unpool_b6', pos=1.25),
    *block_Decoder( name="b7", botton="conv_b6", top='end_b7', s_filer=160, n_filer=64, offset="(1.1,0,0)", size=(25,25,4.5), opacity=0.5 ),
    to_skip( of='clstm_e2', to='unpool_b7', pos=1.25),    
    *block_Decoder( name="b8", botton="conv_b7", top='end_b8', s_filer=320, n_filer=32, offset="(1.1,0,0)", size=(32,32,3.5), opacity=0.5 ),
    to_skip( of='clstm_e1', to='unpool_b8', pos=1.25),    
    
    # Predictors
    to_Conv(name="p", s_filer=640, n_filer=1, offset="(0.75,0,0)", to="(conv_b8-east)", height=40, depth=40, caption="predictor" ),     
    to_skip( of='h', to='p', pos=1.25),   
    to_output( '../depth.png', to='(p-east)', name="640x480x15"),
    to_end() 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
