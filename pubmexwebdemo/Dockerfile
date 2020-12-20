FROM nvidia/cuda:10.1-cudnn7-devel

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y \
	python3-opencv ca-certificates python3-dev git wget sudo && \
  rm -rf /var/lib/apt/lists/*

# create a non-root user
ARG USER_ID=1000
RUN useradd -m --no-log-init --system  --uid ${USER_ID} appuser -g sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER appuser
WORKDIR /home/appuser

ENV PATH="/home/appuser/.local/bin:${PATH}"
RUN wget https://bootstrap.pypa.io/get-pip.py && \
	python3 get-pip.py --user && \
	rm get-pip.py

# install dependencies
# See https://pytorch.org/ for other options if you use a different version of CUDA
RUN pip install --user torch torchvision tensorboard cython
RUN pip install --user 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'

RUN pip install --user 'git+https://github.com/facebookresearch/fvcore'
# install detectron2
RUN git clone https://github.com/facebookresearch/detectron2 detectron2_repo
ENV FORCE_CUDA="1"
# This will build detectron2 for all common cuda architectures and take a lot more time,
# because inside `docker build`, there is no way to tell which architecture will be used.
ENV TORCH_CUDA_ARCH_LIST="Kepler;Kepler+Tesla;Maxwell;Maxwell+Tegra;Pascal;Volta;Turing"
RUN pip install --user -e detectron2_repo

# Set a fixed model cache directory.
ENV FVCORE_CACHE="/tmp"
WORKDIR /home/appuser/detectron2_repo


# Copy everything from current directory to docker work directory.
COPY . .

# If any change made to requirement.txt then copy that again at the time of Docker build.
COPY ./requirements.txt /requirements.txt

# If any change made to static files then copy that again at the time of Docker build.
COPY ./app/static ./app/static

# Give write permission to appuser on app directory.
RUN sudo chown -R appuser ./app

# Create a new directory inside app directory to store uploaded pdf files.
RUN mkdir -p ./app/uploads

# Install poppler in the system path.
RUN sudo apt-get update
RUN sudo apt-get install poppler-utils -y

# Install all the project dependencies one by one.
RUN pip install -r /requirements.txt --use-deprecated=legacy-resolver

# Specify entrypoint with command.
CMD [ "python3", "./app/main.py" ]

# Expose port from inside container for outside access.
EXPOSE 5000
