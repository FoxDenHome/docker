FROM jupyter/tensorflow-notebook:latest

RUN pip install lpips datetime timm ftfy einops pytorch-lightning omegaconf transformers opencv-python
COPY init.py /custom/init.py
RUN python /custom/init.py
