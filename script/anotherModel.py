#coding:utf-8
import mxnet as mx
from mxnet.gluon import HybridBlock
from mxnet.gluon.model_zoo import vision
import numpy as np
from mxnet import nd,autograd
from mxnet.io import NDArrayIter
from mxnet import gluon


ctx = mx.gpu()
alexnet = vision.AlexNet(classes=8)

def transform(labels):
    results = []
    for label in labels:
        label = int(label)-1
        results.append(label)
    return results

#test accuracy
def testAccuracy(net,acc,testIter):
    acc.reset()
    testIter.reset()
    for batch in testIter:
        predict = nd.argmax(nd.softmax(net(batch.data[0].as_in_context(model_ctx))),axis=1)
        acc.update(preds=predict,labels=batch.label[0].as_in_context(model_ctx))
    return acc.get()[1]

trainRatio = 0.75
testRatio = 0.25

spectrumData = np.load('cut_img_list.npy')
dataNum = spectrumData.shape[0]
trainNum = int(dataNum*trainRatio)
testNum = dataNum-trainNum

trainData = nd.array(spectrumData[:trainNum,0].tolist()).reshape((trainNum,1,256,256))
trainLabels = nd.array(transform(spectrumData[:trainNum,1].tolist()))
testData = nd.array(spectrumData[trainNum:,0].tolist()).reshape((testNum,1,256,256))
testLabels = nd.array(transform(spectrumData[trainNum:,1].tolist()))

model_ctx = mx.gpu()
alexnet.collect_params().initialize(mx.init.Xavier(magnitude=2.24), ctx=model_ctx)
softmax_cross_entropy = gluon.loss.SoftmaxCrossEntropyLoss()
trainer = gluon.Trainer(alexnet.collect_params(), 'sgd', {'learning_rate': .001,'wd':1e-5,'momentum':0.9})

trainIter = NDArrayIter(data=trainData,label=trainLabels,batch_size=64,shuffle=True)
testIter = NDArrayIter(data=testData,label = testLabels,batch_size=64,shuffle=True)

epochs= 100
acc = mx.metric.Accuracy() 
accs = []
alexnet.hybridize()
lastAccuracy = 0
curAccuracy = 0
for e in range(epochs):
    acc.reset()
    trainIter.reset()
    i = 0
    outputs = None
    labels = None
    for batch in trainIter:
        data = batch.data[0].as_in_context(model_ctx)
        label = batch.label[0].as_in_context(model_ctx)
        with autograd.record():
            output = alexnet(data)
            loss = softmax_cross_entropy(output, label) 
        loss.backward()
        trainer.step(data.shape[0])
        if i == 0:
            outputs = output
            labels = label
        else:
            outputs = nd.concat(outputs,output,dim=0)
            labels = nd.concat(labels,label,dim=0)
        i+=1
    acc.update(preds=nd.argmax(nd.softmax(outputs),axis=1),labels=labels)
    print("epoch {},training accuracy:{}".format(e,acc.get()[1]))
    if e%10==0:
        curAccuracy = testAccuracy(alexnet,acc,testIter)
        print('curAccuracy is {}, and lastAccuracy is {}'.format(curAccuracy,lastAccuracy))
        if curAccuracy > lastAccuracy:
            print('current testing accuracy:{}'.format(curAccuracy))
            print('saving model......')
            lastAccuracy = curAccuracy
            alexnet.save_params('model_param')



    #print(len(outputs))
print('done')

# print(type(alexnet))