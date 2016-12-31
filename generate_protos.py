import readproto as rp
import sys
import os
sys.path.append("../")
import model_generator.projectroot as prt
proot = prt.project_dir

def find_layer_index(net,layername):
	for i in xrange(len(net.layer)):
		if net.layer[i].name == layername:
			return i

def generate_proto(base_model,new_model,dataname):

	cls_gt_root = os.path.join(proot,"MorpxData",dataname,"clsGTBox")
	numcls = len(os.listdir(cls_gt_root))+1

	train_proto = os.path.join(proot,"base_models",base_model,"train.prototxt")
	test_proto = os.path.join(proot,"base_models",base_model,"test.prototxt")
        solver_proto = os.path.join(proot,"base_models",base_model,"solver.prototxt")


	btrain_net=rp.read_net_proto(train_proto)
	btest_net=rp.read_net_proto(test_proto)

	train_input_data_index=find_layer_index(btrain_net,'input-data')
	btrain_net.layer[train_input_data_index].python_param.param_str="'num_classes': "+str(numcls)

	tr_roidata_index = find_layer_index(btrain_net,'roi-data')
	btrain_net.layer[tr_roidata_index].python_param.param_str="'num_classes': "+str(numcls)
	btrain_net.layer[tr_roidata_index].name = 'roi-data'+"_"+new_model

	bbp_index = find_layer_index(btrain_net,'bbox_pred')
	btrain_net.layer[bbp_index].inner_product_param.num_output=4*numcls
	btrain_net.layer[bbp_index].name='bbox_pred'+"_"+new_model

	cls_score_index = find_layer_index(btrain_net,'cls_score')
	btrain_net.layer[cls_score_index].inner_product_param.num_output = numcls
	btrain_net.layer[cls_score_index].name='cls_score'+"_"+new_model

	lb_index = find_layer_index(btrain_net,'loss_bbox')
	btrain_net.layer[lb_index].name = 'loss_bbox'+"_"+new_model

	lc_index = find_layer_index(btrain_net,'loss_cls')
	btrain_net.layer[lc_index].name = 'loss_cls'+"_"+new_model



	test_bbp_index = find_layer_index(btest_net,'bbox_pred')
        btest_net.layer[test_bbp_index].inner_product_param.num_output=4*numcls
        btest_net.layer[test_bbp_index].name='bbox_pred'+"_"+new_model

	test_cls_score_index = find_layer_index(btest_net,'cls_score')
        btest_net.layer[test_cls_score_index].inner_product_param.num_output = numcls
        btest_net.layer[test_cls_score_index].name='cls_score'+"_"+new_model



	bsolver = rp.read_solver_proto(solver_proto)
	bsolver.train_net = os.path.join(proot,"models",new_model,"train.prototxt")
	
	try:
		os.mkdir( os.path.join(proot,"models",new_model) )
	except OSError:
		pass

	with open(os.path.join(proot,"models",new_model,"train.prototxt"),"w") as f:
		f.write(str(btrain_net))
	f.close()
	
	with open(os.path.join(proot,"models",new_model,"test.prototxt"),"w") as f:
                f.write(str(btest_net))
	f.close()

	with open(os.path.join(proot,"models",new_model,"solver.prototxt"),"w") as f:
                f.write(str(bsolver))
	f.close()


def main(argv=None):
	if argv is None:
		argv = sys.argv

	base_model,new_model,dataname = argv[1:]
	generate_proto(base_model,new_model,dataname)


if __name__ == '__main__':
	main()
