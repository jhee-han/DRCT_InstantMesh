<div align="center">
  
# SR_InstantMesh: Super-resolution Enhanced 3D Mesh Generation from a Single Image Using Sparse-view Large Reconstruction Models.

<a href="https://arxiv.org/abs/2404.07191"><img src="https://img.shields.io/badge/ArXiv-2404.07191-brightgreen"></a> 
<a href="https://huggingface.co/TencentARC/InstantMesh"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Model_Card-Huggingface-orange"></a> 
<a href="https://huggingface.co/spaces/TencentARC/InstantMesh"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Gradio%20Demo-Huggingface-orange"></a> <br>
<a href="https://replicate.com/camenduru/instantmesh"><img src="https://img.shields.io/badge/Demo-Replicate-blue"></a>
<a href="https://colab.research.google.com/github/camenduru/InstantMesh-jupyter/blob/main/InstantMesh_jupyter.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg"></a>
<a href="https://github.com/jtydhr88/ComfyUI-InstantMesh"><img src="https://img.shields.io/badge/Demo-ComfyUI-8A2BE2"></a>

</div>

---

This repo is the official implementation of SR_InstantMesh, where we have fine-tuned IPG and DRCT for super-resolution and InstantMesh for efficient 3D mesh generation from a single image based on the LRM/Instant3D architecture.

https://github.com/TencentARC/InstantMesh/assets/20635237/dab3511e-e7c6-4c0b-bab7-15772045c47d


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

We provide 4 sparse-view reconstruction model variants and a customized Zero123++ UNet for white-background image generation in the [model card](https://huggingface.co/TencentARC/InstantMesh).

Our inference script will download the models automatically. Alternatively, you can manually download the models and put them under the `ckpts/` directory.

By default, we use the `instant-mesh-large` reconstruction model variant.

## Start a local gradio demo

To start a gradio demo in your local machine, simply run:
```bash
python app.py
```

If you have multiple GPUs in your machine, the demo app will run on two GPUs automatically to save memory. You can also force it to run on a single GPU:
```bash
CUDA_VISIBLE_DEVICES=0 python app.py
```

Alternatively, you can run the demo with docker. Please follow the instructions in the [docker](docker/) directory.

## Running with command line

To generate 3D meshes from images via command line, simply run:
```bash
python run.py configs/instant-mesh-large.yaml examples/hatsune_miku.png --save_video
```

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

| Model | Scale | Urban100 | Weights                                                      | Visual Results                                               |
| ----- | ----- | -------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| IPG   | 2x    | 34.48    | [🤗Link](https://huggingface.co/yuchuantian/IPG/blob/main/IPG_SRx2.pth) | [🤗Link](https://huggingface.co/yuchuantian/IPG/blob/main/IPG_srx2.zip) |
| IPG   | 3x    | 30.36    | [🤗Link](https://huggingface.co/yuchuantian/IPG/blob/main/IPG_SRx3.pth) | [🤗Link](https://huggingface.co/yuchuantian/IPG/blob/main/IPG_srx3.zip) |
| IPG   | 4x    | 28.13    | [🤗Link](https://huggingface.co/yuchuantian/IPG/blob/main/IPG_SRx4.pth) | [🤗Link](https://huggingface.co/yuchuantian/IPG/blob/main/IPG_srx4.zip) |

## Weights & Visual Results for DRCT

| [DRCT-XL (pretrained on ImageNet)](https://drive.google.com/file/d/1uLGwmSko9uF82X4OPOMw3xfM3stlnYZ-/view?usp=sharing) | 32.97 / 0.91 | 29.08 / 0.80 | [log](https://drive.google.com/file/d/1kl2r9TbQ8TR-sOdzvCcOZ9eqNsmIldGH/view?usp=drive_link)


# How to use SR_InstantMesh

To generate 3D meshes from images via command line, simply run (After --copy_dir, input DRCT/datasets or IPG/imgs) :
```bash
python run.py configs/instant-mesh-large.yaml /hdd/jhee/3D/SR_InstantMesh/examples/p01_01.png --copy_dir /hdd/jhee/3D/SR_InstantMesh/DRCT/datasets --export_texmap --export_texmap

```

To apply super resolution to an image with the DRCT model:
```bash
cd DRCT
python inference.py --input /hdd/jhee/3D/SR_InstantMesh/DRCT/datasets --output /hdd/jhee/3D/SR_InstantMesh/DRCT/results --model_path /hdd/jhee/3D/SR_InstantMesh/DRCT/pretrained_models/DRCT_SRx4_ImageNet-pretrain.pth

```

If you use the DRCT model for super resolution, you can perform Instant Mesh by running:
```bash
python sr_run.py configs/instant-mesh-large.yaml --export_texmap --drct

```

If you use the IPG model for super resolution, you can perform Instant Mesh by running:
```bash
python sr_run.py configs/instant-mesh-large.yaml --export_texmap --lpg


```


# 🤗 Acknowledgements

We thank the authors of the following projects for their excellent contributions to 3D generative AI!

- [Zero123++](https://github.com/SUDO-AI-3D/zero123plus)
- [OpenLRM](https://github.com/3DTopia/OpenLRM)
- [FlexiCubes](https://github.com/nv-tlabs/FlexiCubes)
- [Instant3D](https://instant-3d.github.io/)

