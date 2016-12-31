import set_caffe_path
import caffe
from caffe.proto import caffe_pb2
from google.protobuf import text_format




def read_net_proto(prototxt):

	net = caffe_pb2.NetParameter()

	file=open(prototxt,"r")
	text_format.Merge(str(file.read()),net)

	return net

def read_solver_proto(prototxt):
	
	solver=caffe_pb2.SolverParameter()
	
	file=open(prototxt,"r")
	
	text_format.Merge(str(file.read()),solver)
	
	return solver

if __name__ == '__main__':
	
	prototxt="/home/henry/projects/python/pycaffe/model_generator/py-faster-rcnn/models/pascal_voc/ZF/faster_rcnn_end2end/train.prototxt"
	net=read_net_proto(prototxt)
	print net.layer[1].top
	#print  getattr(net.layer[0],"python_param").param_str.strip().split(":")[1]
	with open("/home/henry/train.txt","w") as f:
		f.write(str(net))