# start from base
FROM continuumio/anaconda3
MAINTAINER Roma Kail <roman.kail@mail.ru>
USER root

# updating system
RUN apt-get -yqq update &&  apt-get -yqq upgrade

# system tools
RUN apt-get install -yqq gcc g++ libstdc++6 curl wget unzip git \
                         tmux nano watch vim kmod htop fish \
                         libopenblas-dev liblapack-dev libsdl2-dev libboost-all-dev graphviz \
                         cmake zlib1g-dev libjpeg-dev \
                         xvfb xorg-dev python-opengl python3-opengl
# RUN apt-get install -yqq swig3.0
# RUN ln -s /usr/bin/swig3.0 /usr/bin/swig

# python3 libraries
RUN pip install -U pip
RUN pip install --upgrade aiogram beautifulsoup4 google
# RUN pip install --upgrade tabulate tqdm editdistance joblib graphviz gensim matplotlib tensorboardX wget
# RUN pip install --upgrade sklearn nltk pandas numpy scipy xgboost
# RUN pip install torch torchvision
# RUN pip install pytorch-transformers torchsummary
# RUN pip install jupyterlab

# git configures
# RUN git config --global user.email "roman.kail@mail.ru" && \
###    git config --global user.name  "romakail"
RUN git clone https://github.com/romakail/Cinema-Bot
RUN chmod +x ./Cinema-Bot/cinema_bot.py
# setting the terminal
RUN chsh -s `which fish`

# creating entry script
ADD launch_script.sh ./launch_script.sh
RUN chmod +x ./launch_script.sh
ENTRYPOINT "./launch_script.sh"
# ENTRYPOINT ["ls"]
