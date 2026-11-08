import json,sys,numpy as np,onnxruntime as ort,wave
M='/tmp/v_voice-fr-siwis-medium/fr-siwis-medium.onnx'
cfg=json.load(open(M+'.json'));pm=cfg['phoneme_id_map'];sr=cfg['audio']['sample_rate']
sess=ort.InferenceSession(M,providers=['CPUExecutionProvider'])
def ids(ph):
    out=pm['^']+pm['_']
    for c in ph:
        if c in pm: out+=pm[c]+pm['_']
    return out+pm['$']
def synth(ph,path,ls=1.1,noise=0.5,nw=0.6):
    x=np.array([ids(ph)],dtype=np.int64)
    a=sess.run(None,{'input':x,'input_lengths':np.array([x.shape[1]],dtype=np.int64),'scales':np.array([noise,ls,nw],dtype=np.float32)})[0].squeeze()
    a=np.clip(a/ max(1e-6,np.abs(a).max())*0.9,-1,1)
    with wave.open(path,'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((a*32767).astype(np.int16).tobytes())
    return len(a)/sr
if __name__=='__main__':
    for ph,name in [('mːːː','m'),('sːːː','s'),('aː','a'),('yː','u'),('ʃːːː','ch'),('pə','p'),('mːːaːː','mmmaaa'),('ma','ma'),('ʁːːː','r')]:
        print(name, round(synth(ph,f'/tmp/ph/{name}.wav'),2))
