# 使用 Amazon SageMaker 训练自己的数据
 
常用的机器学习的DEMO或者演示项目中使用到的基本全是公开已经制作好并经过经验的数据集，而工作中实际运用到生产的数据往往是未经过处理的。这个项目演示了如何从零开始（指手头没有任何数据），收集数据，筛选数据，给数据打标签，并通过有限数量的jpeg图片（3000张图片），生成 MXNet 常用的 RecordIO 数据格式。并利用自定义的小规模数据集，进行迁移学习（transfer learning），在短时间低成本的情况下获取准确率较高的模型。

另外，可以使用上述生成的数据集交给 Amazon SageMaker Ground Truth 快速进行数据打标签的测试。

## Tranfer learning 迁移学习
`./transfer-learning-setup.sh`
在 Amazon SageMaker 中打开notebook 'Image-classification-transfer-learning-highlevel.ipynb'，参照步骤进行迁移学习
训练完成后可以运行 `./transfer-learning-clean.sh` 清空目录下不需要的文件

## 测试 Amazon SageMaker Ground Truth
`./ground-truth-setup.sh`
在 Amazon SageMaker Ground Truth 中按照页面中的步骤创建项目，其中数据的输入文件复制命令行脚本的输出结果。
提交打标签任务后，可以运行`./ground-truth-clean.sh` 清空不必要的文件并删除S3存储桶
