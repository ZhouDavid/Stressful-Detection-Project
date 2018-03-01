import numpy as np
import mxnet as mx
from mxnet import nd,autograd
from mxnet import gluon
from mxnet.gluon import Block,nn,HybridBlock
from mxnet.io import NDArrayIter

class EmotionModel(HybridBlock):
    def __init__(self,**kwargs):
        super(EmotionModel,self).__init__(**kwargs)
        with self.name_scope():
            # self.conv1 = nn.Conv2D(channels=96,kernel_size=(11,11),strides=(4,4))
            # self.maxpool1 = nn.MaxPool2D(pool_size=(3,3),strides=2)
            # self.conv2 = nn.Conv2D(channels=256,kernel_size=5,padding=2,groups=2)
            # self.maxpool2 = nn.MaxPool2D(pool_size=3,strides=2)
            # self.conv3 = nn.Conv2D(channels=384,kernel_size=1,padding=1)
            # self.conv4 = nn.Conv2D(channels=384,kernel_size=3,padding=1)
            # self.conv5 = nn.Conv2D(channels=256,kernel_size=3,padding=1)
            # self.maxpool5=nn.MaxPool2D(pool_size=3,strides=2)
            # self.dense6=nn.Dense(4096)
            # self.drop6 = nn.Dropout(0.5)
            # self.dense7 = nn.Dense(4096)
            # self.drop7=nn.Dropout(0.5)
            # self.dense8=nn.Dense(8)

    def hybrid_forward(self,F,x):
        x = F.relu(self.conv1(x))
        x = self.maxpool1(x)
        x = F.relu(self.conv2(x))
        x = self.maxpool2(x)
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = F.relu(self.conv5(x))
        x = self.maxpool5(x)
        x = self.dense6(x)
        x = self.drop6(x)
        x = self.dense7(x)
        x = self.drop7(x)
        x = self.dense8(x)
        return x

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

alexModel = EmotionModel()
model_ctx = mx.gpu()
alexModel.collect_params().initialize(mx.init.Xavier(magnitude=2.24), ctx=model_ctx)
softmax_cross_entropy = gluon.loss.SoftmaxCrossEntropyLoss()
trainer = gluon.Trainer(alexModel.collect_params(), 'sgd', {'learning_rate': .0001,'wd':1e-5,'momentum':0.9})

trainIter = NDArrayIter(data=trainData,label=trainLabels,batch_size=64,shuffle=True)
testIter = NDArrayIter(data=testData,label = testLabels,batch_size=64,shuffle=True)

epochs= 100
acc = mx.metric.Accuracy() 
accs = []
alexModel.hybridize()
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
            output = alexModel(data)
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
        curAccuracy = testAccuracy(alexModel,acc,testIter)
        print('curAccuracy is {}, and lastAccuracy is {}'.format(curAccuracy,lastAccuracy))
        if curAccuracy > lastAccuracy:
            print('current testing accuracy:{}'.format(curAccuracy))
            print('saving model......')
            lastAccuracy = curAccuracy
            alexModel.export('model')



    #print(len(outputs))
print('done')