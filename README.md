<div align="center">
  
# SR_InstantMesh: Super-resolution Enhanced 3D Mesh Generation from a Single Image Using Sparse-view Large Reconstruction Models.

<div >
---

This repo is the official implementation of SR_InstantMesh, where we have fine-tuned IPG and DRCT for super-resolution and InstantMesh for efficient 3D mesh generation from a single image based on the LRM/Instant3D architecture.


# ⚙️ Dependencies and Installation

We recommend used `Python>=3.10`, `PyTorch>=2.1.0`, and `CUDA=11.8`.
```bash
conda create --name sr_instantmesh python=3.10
conda activate sr_instantmesh
pip install -U pip

# Ensure Ninja is installed
conda install Ninja

# Install the correct version of CUDA
conda install cuda -c nvidia/label/cuda-12.1.0

# Install PyTorch and xformers
# You may need to install another xformers version if you use a different PyTorch version
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu118
pip install xformers==0.0.22.post4 --index-url https://download.pytorch.org/whl/cu118

# For Linux users: Install Triton 
pip install triton

# For Windows users: Use the prebuilt version of Triton provided here:
pip install https://huggingface.co/r4ziel/xformers_pre_built/resolve/main/triton-2.0.0-cp310-cp310-win_amd64.whl

# Install other requirements
pip install -r requirements.txt

#Install requirements for DRCT
cd DRCT
pip install -r requirements.txt
python setup.py develop

#Install requirements for IPG
#The version of wheel you're using (0.26.0) is quite old, which might be causing compatibility issues.
#Update both packages to the latest versions:
#pip install --upgrade setuptools wheel

cd ..
cd IPG
pip install wheel==0.26 
pip install -r requirements.txt
python setup.py install
```

# 💫 How to Use

## Download the models for InstantMesh

Our inference script will download the models automatically. Alternatively, you can manually download the models and put them under the `ckpts/` directory.

By default, we use the `instant-mesh-large` reconstruction model variant.

We use [rembg](https://github.com/danielgatis/rembg) to segment the foreground object. If the input image already has an alpha mask, please specify the `no_rembg` flag:
```bash
python run.py configs/instant-mesh-large.yaml examples/hatsune_miku.png --save_video --no_rembg
```

By default, our script exports a `.obj` mesh with vertex colors, please specify the `--export_texmap` flag if you hope to export a mesh with a texture map instead (this will cost longer time):
```bash
python run.py configs/instant-mesh-large.yaml examples/hatsune_miku.png --save_video --export_texmap
```

Please use a different `.yaml` config file in the [configs](./configs) directory if you hope to use other reconstruction model variants. For example, using the `instant-nerf-large` model for generation:
```bash
python run.py configs/instant-nerf-large.yaml examples/hatsune_miku.png --save_video
```
**Note:** When using the `NeRF` model variants for image-to-3D generation, exporting a mesh with texture map by specifying `--export_texmap` may cost long time in the UV unwarping step since the default iso-surface extraction resolution is `256`. You can set a lower iso-surface extraction resolution in the config file.


## Weights & Visual Results for IPG

By default, we use a 4× scale. Please download the weights from the link below and place them inside the IPG folder.

| Model | Scale | Urban100 | Weights                                                      | Visual Results                                               |
| ----- | ----- | -------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| IPG   | 2x    | 34.48    | [🤗Link](https://huggingface.co/yuchuantian/IPG/blob/main/IPG_SRx2.pth) | [🤗Link](https://huggingface.co/yuchuantian/IPG/blob/main/IPG_srx2.zip) |
| IPG   | 3x    | 30.36    | [🤗Link](https://huggingface.co/yuchuantian/IPG/blob/main/IPG_SRx3.pth) | [🤗Link](https://huggingface.co/yuchuantian/IPG/blob/main/IPG_srx3.zip) |
| IPG   | 4x    | 28.13    | [🤗Link](https://huggingface.co/yuchuantian/IPG/blob/main/IPG_SRx4.pth) | [🤗Link](https://huggingface.co/yuchuantian/IPG/blob/main/IPG_srx4.zip) |

## Weights & Visual Results for DRCT

Please download the pretrained model from the link below and place them inside the DRCT/experiments/pretrained_models.

| [DRCT-XL (pretrained on ImageNet)](https://drive.google.com/file/d/1uLGwmSko9uF82X4OPOMw3xfM3stlnYZ-/view?usp=sharing) | 32.97 / 0.91 | 29.08 / 0.80 | [log](https://drive.google.com/file/d/1kl2r9TbQ8TR-sOdzvCcOZ9eqNsmIldGH/view?usp=drive_link)

# Things to do before running the model

1. Download the weights for IPG (skip this step if you are only using the DRCT model).
2. Download the pretrained model for DRCT (skip this step if you are only using the IPG model).
3. Remove every README.md file.
4. In `SR_InstantMesh/IPG/options/test_mod/test_IPG_SR_x4.yml`, change the paths for `dataroot_lq` and `pretrain_network_g`.

Once everything is ready, refer to "How to use SR_InstantMesh" to run the model.

# How to use SR_InstantMesh

To generate a 3D mesh using the DRCT model, simply run:
```bash
python sr_instantmesh.py --method drct --input_image /path/to/the/input_image.png --output_dir /path/to/the/output_dir --drct_model /path/to/the/pretrained_models.pth
```

To generate a 3D mesh using the DRCT model, simply run:
```bash
python sr_instantmesh.py --method drct --input_image /path/to/the/input_image.png --output_dir /path/to/the/output_dir --drct_model /path/to/the/pretrained_models.pth
```



# 🤗 Acknowledgements

We thank the authors of the following projects for their excellent contributions to 3D generative AI!

- [DRTC](https://github.com/ming053l/DRCT)
- [InstantMesh](https://instant-3d.github.io/)
- [IPG](https://github.com/huawei-noah/Efficient-Computing/tree/master/LowLevel/IPG)
- [Zero123++](https://github.com/SUDO-AI-3D/zero123plus)
- [OpenLRM](https://github.com/3DTopia/OpenLRM)
- [FlexiCubes](https://github.com/nv-tlabs/FlexiCubes)
- [Instant3D](https://instant-3d.github.io/)


