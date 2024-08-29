<div align="center">
  
# DRCT_InstantMesh: Super-resolution Enhanced 3D Mesh Generation from a Single Image Using Sparse-view Large Reconstruction Models.

</div>

---

This repo is the official implementation of SR_InstantMesh, where we have applied DRCT for super-resolution and InstantMesh for efficient 3D mesh generation from a single image based on the LRM/Instant3D architecture.


# ⚙️ Dependencies and Installation

We recommend used `Python>=3.10`, `PyTorch>=2.1.0`, and `CUDA>=11.8`.
```bash
conda create --name drct_instantmesh python=3.10 -y
conda activate drct_instantmesh
pip install -U pip

# Ensure Ninja is installed
conda install Ninja

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
#If you got ImportError: cannot import name 'split_torch_state_dict_into_shards' from 'huggingface_hub', pip install --upgrade huggingface_hub
cd DRCT
pip install -r requirements.txt
python setup.py develop

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

## Weights & Visual Results for DRCT

Please download the pretrained model from the link below and place them inside the DRCT/experiments/pretrained_models.

| [DRCT-L ]([https://drive.google.com/file/d/1uLGwmSko9uF82X4OPOMw3xfM3stlnYZ-/view?usp=sharing](https://drive.google.com/file/d/1bVxvA6QFbne2se0CQJ-jyHFy94UOi3h5/view?usp=sharing) 

# Things to do before running the model

1. Download the pretrained model for DRCT (Skip this step if you are only using the IPG model).
2. Remove every README.md file.
EX) DRCT/datasets/README.md, DRCT/experiments/pretrained_models/README.md, DRCT/results/README.md
4. If you want to run DRCT once and then execute sr_instantmesh with a different input image, make sure to delete all contents inside the following directories so that they are empty: `/DRCT/datasets`, `/DRCT/results` 
You can delete at once by 'python clean.py'

Once everything is ready, refer to "How to use DRCT_InstantMesh" to run the model.

# How to use DRCT_InstantMesh

To generate a 3D mesh using the DRCT model, simply run:
```bash
python sr_instantmesh.py --method drct --input_image /path/to/the/input_image.png --output_dir /path/to/the/output_dir/DRCT/results --drct_model /path/to/the/experiments/pretrained_models/pretrained_model.pthpretrained_models.pth
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


