# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import math
from . import blueprint
# Flask modules
import plotly.subplots as sp
from flask import render_template, request, url_for, redirect, send_from_directory, jsonify, make_response
from flask_table import Table, Col, LinkCol
from functools import partial
import json
import time
from scipy.spatial.distance import pdist
pw_jaccard_func = partial(pdist, metric='jaccard')
import scipy.cluster.hierarchy as sch
import random
from wordcloud import WordCloud, STOPWORDS
from pytimeparse.timeparse import timeparse
import matplotlib.pyplot as plt
import time
import pyLDAvis.gensim
import nltk
from nltk.corpus import stopwords
import plotly.express as px
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import RegexpTokenizer
from gensim import corpora, models
import gensim
from plotly.subplots import make_subplots
import os
from os import path
from time import sleep
from matplotlib.figure import Figure
from dash_holoniq_wordcloud import DashWordcloud
from dash import Dash, dcc, html
from bs4 import BeautifulSoup
import plotly.graph_objs as go
import csv
from collections import defaultdict
import string
stop_words = set(stopwords.words("english"))
from collections import OrderedDict
from plotly import exceptions, optional_imports
from plotly.graph_objs import graph_objs
from distinctipy import distinctipy
np = optional_imports.get_module("numpy")
scp = optional_imports.get_module("scipy")
sch = optional_imports.get_module("scipy.cluster.hierarchy")
scs = optional_imports.get_module("scipy.spatial")
import numpy as np
np.random.seed(1)
import plotly
import pandas as pd
import pickle
import seaborn as sns 
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.figure_factory as ff
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import dendrogram, linkage, cut_tree
from collections import namedtuple
from json import JSONEncoder

from bigtree import Node, print_tree, dataframe_to_tree, tree_to_dataframe
from datetime import datetime
from datetime import timezone
import datetime
import networkx as nx
from scipy.spatial.distance import jaccard, squareform

from bertopic import BERTopic
from plotly.graph_objs import *

global threshold
global glo_dataframes
from eventregistry import *

threshold = 0.2
dendro_clusters = 0
color_ran = []

selected_event = ""
selected_barrier = ""
dbfileName = 'data/ForPropagationNetworkNew2.csv'
total_clusters = 0
clustered_dataframes = pd.DataFrame()

colors = ["blue",  "black",  "brown", "gray", "green", "orange", "purple", "red", "white", "yellow", "bisque",
                "burlywood", "chartreuse", "chocolate", "coral", "cornsilk", "crimson", "darkblue", "darkcyan", "darkgoldenrod", "darkgray", 
                "darkgreen", "darkkhaki", "darkmagenta", "darkolivegreen", "darkorange", "darkorchid", "darkred", "darksalmon", "darkseagreen",
                "darkslateblue", "darkslategray", "darkslategrey", "darkturquoise", "darkviolet", "deeppink", "deepskyblue",
                "dimgray", "dodgerblue", "firebrick", "floralwhite", "forestgreen", "fuchsia", "gainsboro",
                "ghostwhite", "gold", "goldenrod",  "greenyellow", "honeydew", "hotpink", "indianred",
                "indigo", "ivory", "khaki", "lavender", "lavenderblush", "lawngreen", "lemonchiffon", "lightblue", "lightcoral", 
                "lightcyan", "lightgoldenrodyellow", "lightgray", "lightgreen", "lightpink", "lightsalmon", 
                "lightseagreen", "lightskyblue", "lightslategray", "lightsteelblue", "lightyellow", "lime",
                "limegreen", "linen", "magenta", "maroon", "mediumaquamarine", "mediumblue", "mediumorchid", "mediumpurple",
                "mediumseagreen", "mediumslateblue", "mediumspringgreen", "mediumturquoise", "mediumvioletred", "midnightblue",
                "mintcream", "mistyrose", "moccasin", "navajowhite", "navy", "oldlace", "olive", "olivedrab", 
                "orangered", "orchid", "palegoldenrod", "palegreen", "paleturquoise", "palevioletred", "papayawhip", "peachpuff",
                "peru", "pink", "plum", "powderblue",  "rosybrown", "royalblue", "rebeccapurple", "saddlebrown",
                "salmon", "sandybrown", "seagreen", "seashell", "sienna", "silver", "skyblue", "slateblue", "slategray",
                "slategrey", "snow", "springgreen", "steelblue", "tan", "teal", "thistle", "violet"] 



# KEY = "b198299a-bb74-4eab-8d59-9dc1fc3679c2",
#KEY = "0ec67093-425f-4d84-b9e9-41bba6de6c71"
#KEY = "041e85db-cf3a-481c-8559-45f4b45ee47a",
KEY = "07a9d524-0986-4aaf-a597-8ec41e86864a"
#KEY = "f3d1fe1a-addb-48f9-a8bc-29daa318df33",
# KEY = "c6022edb-151a-429b-9d23-32f34b4a39ab",
# KEY = "0ec67093-425f-4d84-b9e9-41bba6de6c71",
er = EventRegistry(apiKey=KEY)

all_events = {
        "eng-8467663":"One dead as Cyclone Freddy lashes Mozambique for second time",
        "eng-8468195":"Indonesia's Merapi volcano erupts, blankets villages in ash",
        "eng-8468865":"Flooding inundates Central California communities, blocking routes out",
        "eng-8471915":"UN implicated in Syria aid failures after earthquake -commission", 
        "eng-8472550":"UN urges world to contribute 'as generously as possible' to appeal for quake-hit Türkiye",
        
        "eng-8469535":"IND v AUS, Ahmedabad Test, Day 4: Virat Kohli inches closer to century as India look to take lead", 
        "eng-8470156":"Vote for our Player of the Match v Fulham", 
        "eng-8470041":"Real Madrid vs Liverpool: Prediction, kick-off time, TV, live stream, team news, h2h results, odds", 
        
        "eng-8452523":"UK could be set for coldest temperature of the year as yellow warnings for snow are brought forward", 
        "eng-8471343":"Governments to vet crucial UN climate science report",

        "eng-8451923":"Police reach ex Pakistan PM Khan's residence with arrest warrant", 
        "eng-8452217":"How Are Trump Supporters Still Doing This?", 
        
        "eng-8454149": "iPhone 14 unveiled in yellow - here's your first look", 
        "eng-8452485":"Opinion | Ford vs. Tesla: Guess Which One Is More Old-Fashioned",
        "eng-8455972":"Meta planning thousands of more cuts after widespread layoffs, report says",
        "eng-8468237":"SpaceX Dragon capsule splashes down with Crew-5 astronauts after 157 days in space",

        "rus-1420574":"Российским футболистам нашли турнир по санкциям", 
        "rus-1417054":"Первые ЗРК Patriot прибыли на Украину",
        "eng-8456354":"Austin makes unannounced visit to Baghdad before 20th anniversary of invasion of Iraq",
        "eng-8454935":"Israeli forces kill six Palestinians in latest raid on Jenin", 
        "eng-8470679":"Report: Ukraine world's 3rd biggest arms importer in 2022"}


contractions = { 
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he's": "he is",
"how'd": "how did",
"how'll": "how will",
"how's": "how is",
"i'd": "i would",
"i'll": "i will",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'll": "it will",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"must've": "must have",
"mustn't": "must not",
"needn't": "need not",
"oughtn't": "ought not",
"shan't": "shall not",
"sha'n't": "shall not",
"she'd": "she would",
"she'll": "she will",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"that'd": "that would",
"that's": "that is",
"there'd": "there had",
"there's": "there is",
"they'd": "they would",
"they'll": "they will",
"they're": "they are",
"they've": "they have",
"wasn't": "was not",
"we'd": "we would",
"we'll": "we will",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"where'd": "where did",
"where's": "where is",
"who'll": "who will",
"who's": "who is",
"won't": "will not",
"wouldn't": "would not",
"you'd": "you would",
"you'll": "you will",
"you're": "you are"
}


@blueprint.route('/get_piechart_datafdg')
def get_piechart_datafdg():
    return "data/10NewsArticles.csv"
    contract_labels = ['Month-to-month', 'One year', 'Two year']
    _ = churn_df.groupby('Contract').size().values
    class_percent = calculate_percentage(_, np.sum(_))  # Getting the value counts and total

    piechart_data = []
    data_creation(piechart_data, class_percent, contract_labels)
    return jsonify(piechart_data)


def calculate_percentage(val, total):
    """Calculates the percentage of a value over a total"""
    percent = np.round((np.divide(val, total) * 100), 2)
    return percent


def data_creation(data, percent, class_labels, group=None):
    for index, item in enumerate(percent):
        data_instance = {}
        data_instance['category'] = class_labels[index]
        data_instance['value'] = item
        data_instance['group'] = group
        data.append(data_instance)


def jaccard_dissimilarity(feature_list1, feature_list2, filler_val): #binary
    all_features = set([i for i in feature_list1 if i != filler_val])#filler val can be used to even up ragged lists and ignore certain dtypes ie prots not in a module
    all_features.update(set([i for i in feature_list2 if i != filler_val]))#works for both numpy arrays and lists
    counts_1 = [1 if feature in feature_list1 else 0 for feature in all_features]
    counts_2 = [1 if feature in feature_list2 else 0 for feature in all_features]
    return jaccard(counts_1, counts_2)

def data_to_dist_matrix(mn_data, filler_val = 0):
    distance_matrix = np.array([[jaccard_dissimilarity(a,b, filler_val) for b in mn_data] for a in mn_data])
    return squareform(distance_matrix)


@blueprint.route('/get_piechart_data')
def get_piechart_data():
    contract_labels = ['Month-to-month', 'One year', 'Two year']
    _ = churn_df.groupby('Contract').size().values
    class_percent = calculate_percentage(_, np.sum(_)) 

    piechart_data = []
    data_creation(piechart_data, class_percent, contract_labels)
    return jsonify(piechart_data)


@blueprint.route('/get_barchart_data')
def get_barchart_data():
    tenure_labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79']
    churn_df['tenure_group'] = pd.cut(churn_df.tenure, range(0, 81, 10), labels=tenure_labels)
    select_df = churn_df[['tenure_group', 'Contract']]
    contract_month = select_df[select_df['Contract'] == 'Month-to-month']
    contract_one = select_df[select_df['Contract'] == 'One year']
    contract_two = select_df[select_df['Contract'] == 'Two year']
    _ = contract_month.groupby('tenure_group').size().values
    mon_percent = calculate_percentage(_, np.sum(_))
    _ = contract_one.groupby('tenure_group').size().values
    one_percent = calculate_percentage(_, np.sum(_))
    _ = contract_two.groupby('tenure_group').size().values
    two_percent = calculate_percentage(_, np.sum(_))
    _ = select_df.groupby('tenure_group').size().values
    all_percent = calculate_percentage(_, np.sum(_))

    barchart_data = []
    data_creation(barchart_data, all_percent, tenure_labels, "All")
    data_creation(barchart_data, mon_percent, tenure_labels, "Month-to-month")
    data_creation(barchart_data, one_percent, tenure_labels, "One year")
    data_creation(barchart_data, two_percent, tenure_labels, "Two year")
    return jsonify(barchart_data)


@blueprint.route('/')
def dashboard():
    print("ad dashboard")
    return render_template('layouts/default.html', content=render_template('pages/index.html'))


@blueprint.route('/bar_chart')
def bar_chart():
    return render_template('layouts/default.html',
                           content=render_template('pages/barChart.html'))


@blueprint.route('/force_directed_graph')
def force_directed_graph():
    print("force_directed_graph")
    return render_template('layouts/default.html', content=render_template('pages/forceDG.html'))


@blueprint.route('/Community')
def Community():
    return render_template('layouts/default.html',
                           content=render_template('pages/Community.html'))


@blueprint.route('/Radial')
def Radial():
    return render_template('layouts/default.html',
                           content=render_template('pages/Radial.html'))

@blueprint.route('/index.html')
@blueprint.route('/<path>')
def index(path):
    content = None
    try:
        return render_template('layouts/default.html',
                               content=render_template('pages/' + path))

    except:
        return render_template('layouts/auth-default.html',
                               content=render_template('pages/404.html'))

# Return sitemap
@blueprint.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, '../static'), 'sitemap.xml')

@blueprint.route('/aboutus', methods=['GET', 'POST'])
def aboutus():
    return render_template('layouts/default.html',
                           content=render_template("pages/aboutus.html"))

@blueprint.route('/QA', methods=['GET', 'POST'])
def QA():
    return render_template('layouts/default.html',
                           content=render_template("pages/QA.html"))

@blueprint.route('/HC', methods=['GET', 'POST'])
def HC():
    return render_template('layouts/default.html',
                           content=render_template("pages/HC.html"))

@blueprint.route('/word_trends', methods=['GET', 'POST'])
def word_trends():
    return render_template('layouts/default.html',
                           content=render_template("pages/word_trends.html"))

@blueprint.route('/topic_mod', methods=['GET', 'POST'])
def topic_mod():
    return render_template('layouts/default.html',
                           content=render_template("pages/topic_mod.html"))

@blueprint.route('/sent_anly', methods=['GET', 'POST'])
def sent_anly():
    return render_template("/pages/sent_anly.html")

def modified_dendrogram_traces(self, X, colorscale, distfun, linkagefun, hovertext, color_threshold):
    """
    Calculates all the elements needed for plotting a dendrogram.

    :param (ndarray) X: Matrix of observations as array of arrays
    :param (list) colorscale: Color scale for dendrogram tree clusters
    :param (function) distfun: Function to compute the pairwise distance
                               from the observations
    :param (function) linkagefun: Function to compute the linkage matrix
                                  from the pairwise distances
    :param (list) hovertext: List of hovertext for constituent traces of dendrogram
    :rtype (tuple): Contains all the traces in the following order:
        (a) trace_list: List of Plotly trace objects for dendrogram tree
        (b) icoord: All X points of the dendrogram tree as array of arrays
            with length 4
        (c) dcoord: All Y points of the dendrogram tree as array of arrays
            with length 4
        (d) ordered_labels: leaf labels in the order they are going to
            appear on the plot
        (e) P['leaves']: left-to-right traversal of the leaves

    """
    d = distfun(X)
    Z = linkagefun(d)
    P = sch.dendrogram(
        Z,
        orientation=self.orientation,
        labels=self.labels,
        no_plot=True,
        color_threshold=color_threshold,
        truncate_mode = 'level',
        p = 10
    )

    icoord = scp.array(P["icoord"])
    dcoord = scp.array(P["dcoord"])
    ordered_labels = scp.array(P["ivl"])
    color_list = scp.array(P["color_list"])
    colors = self.get_color_dict(colorscale)

    trace_list = []

    for i in range(len(icoord)):
        if self.orientation in ["top", "bottom"]:
            xs = icoord[i]
        else:
            xs = dcoord[i]

        if self.orientation in ["top", "bottom"]:
            ys = dcoord[i]
        else:
            ys = icoord[i]
        color_key = color_list[i]
        hovertext_label = None
        if hovertext:
            hovertext_label = hovertext[i]
        trace = dict(
            type="scatter",
            x=np.multiply(self.sign[self.xaxis], xs),
            y=np.multiply(self.sign[self.yaxis], ys),
            mode="lines",
            marker=dict(color=colors[color_key]),
            text=hovertext_label,
            hoverinfo="text",
        )

        try:
            x_index = int(self.xaxis[-1])
        except ValueError:
            x_index = ""

        try:
            y_index = int(self.yaxis[-1])
        except ValueError:
            y_index = ""

        trace["xaxis"] = "x" + x_index
        trace["yaxis"] = "y" + y_index

        trace_list.append(trace)

    return trace_list, icoord, dcoord, ordered_labels, P["leaves"]

def create_dendrogram2(
    X,
    orientation="bottom",
    labels=None,
    colorscale=None,
    distfun=None,
    linkagefun=lambda x: sch.linkage(x, "complete"),
    hovertext=None,
    color_threshold=None,
    **kwargs
):
    if not scp or not scs or not sch:
        raise ImportError(
            "FigureFactory.create_dendrogram requires scipy, \
                            scipy.spatial and scipy.hierarchy"
        )

    s = X.shape
    if len(s) != 2:
        exceptions.PlotlyError("X should be 2-dimensional array.")

    if distfun is None:
        distfun = scs.distance.pdist

    dendrogram = _Dendrogram(
        X,
        orientation,
        labels,
        colorscale,
        distfun=distfun,
        linkagefun=linkagefun,
        hovertext=hovertext,
        color_threshold=color_threshold,
        kwargs=kwargs
    )

    return graph_objs.Figure(data=dendrogram.data, layout=dendrogram.layout)

class _Dendrogram(object):
    """Refer to FigureFactory.create_dendrogram() for docstring."""

    def __init__(self,X,orientation="bottom",labels=None,colorscale=None,width=np.inf,height=np.inf,xaxis="xaxis",yaxis="yaxis",distfun=None,linkagefun=lambda x: sch.linkage(x, "complete"),hovertext=None,color_threshold=None,kwargs=None):
        self.orientation = orientation
        self.labels = labels
        self.xaxis = xaxis
        self.yaxis = yaxis
        self.data = []
        self.leaves = []
        self.sign = {self.xaxis: 1, self.yaxis: 1}
        self.layout = {self.xaxis: {}, self.yaxis: {}}

        if self.orientation in ["left", "bottom"]:
            self.sign[self.xaxis] = 1
        else:
            self.sign[self.xaxis] = -1

        if self.orientation in ["right", "bottom"]:
            self.sign[self.yaxis] = 1
        else:
            self.sign[self.yaxis] = -1

        if distfun is None:
            distfun = scs.distance.pdist

        (dd_traces, xvals, yvals, ordered_labels, leaves) = self.get_dendrogram_traces(
            X, colorscale, distfun, linkagefun, hovertext, color_threshold, kwargs
        )

        self.labels = ordered_labels
        self.leaves = leaves
        yvals_flat = yvals.flatten()
        xvals_flat = xvals.flatten()

        self.zero_vals = []

        for i in range(len(yvals_flat)):
            if yvals_flat[i] == 0.0 and xvals_flat[i] not in self.zero_vals:
                self.zero_vals.append(xvals_flat[i])

        if len(self.zero_vals) > len(yvals) + 1:
            l_border = int(min(self.zero_vals))
            r_border = int(max(self.zero_vals))
            correct_leaves_pos = range(
                l_border, r_border + 1, int((r_border - l_border) / len(yvals))
            )
            self.zero_vals = [v for v in correct_leaves_pos]

        self.zero_vals.sort()
        self.layout = self.set_figure_layout(width, height)
        self.data = dd_traces

    def get_color_dict(self, colorscale):
        """
        Returns colorscale used for dendrogram tree clusters.

        :param (list) colorscale: Colors to use for the plot in rgb format.
        :rtype (dict): A dict of default colors mapped to the user colorscale.

        """
        d = {
            "r": "red",
            "g": "green",
            "b": "blue",
            "c": "cyan",
            "m": "magenta",
            "y": "yellow",
            "k": "black",
            "w": "white",
        }
        default_colors = OrderedDict(sorted(d.items(), key=lambda t: t[0]))

        if colorscale is None:
            rgb_colorscale = [
                "rgb(0,116,217)",  # blue
                "rgb(35,205,205)",  # cyan
                "rgb(61,153,112)",  # green
                "rgb(40,35,35)",  # black
                "rgb(133,20,75)",  # magenta
                "rgb(255,65,54)",  # red
                "rgb(255,255,255)",  # white
                "rgb(255,220,0)",  # yellow
            ]
        else:
            rgb_colorscale = colorscale

        for i in range(len(default_colors.keys())):
            k = list(default_colors.keys())[i]  # PY3 won't index keys
            if i < len(rgb_colorscale):
                default_colors[k] = rgb_colorscale[i]
        new_old_color_map = [
            ("C0", "b"),
            ("C1", "g"),
            ("C2", "r"),
            ("C3", "c"),
            ("C4", "m"),
            ("C5", "y"),
            ("C6", "k"),
            ("C7", "g"),
            ("C8", "r"),
            ("C9", "c"),
        ]
        for nc, oc in new_old_color_map:
            try:
                default_colors[nc] = default_colors[oc]
            except KeyError:
                default_colors[nc] = "rgb(0,116,217)"

        return default_colors

    def set_axis_layout(self, axis_key):
        """
        Sets and returns default axis object for dendrogram figure.

        :param (str) axis_key: E.g., 'xaxis', 'xaxis1', 'yaxis', yaxis1', etc.
        :rtype (dict): An axis_key dictionary with set parameters.

        """
        axis_defaults = {
            "type": "linear",
            "ticks": "outside",
            "mirror": "allticks",
            "rangemode": "tozero",
            "showticklabels": True,
            "zeroline": False,
            "showgrid": False,
            "showline": True,
        }

        if len(self.labels) != 0:
            axis_key_labels = self.xaxis
            if self.orientation in ["left", "right"]:
                axis_key_labels = self.yaxis
            if axis_key_labels not in self.layout:
                self.layout[axis_key_labels] = {}
            self.layout[axis_key_labels]["tickvals"] = [
                zv * self.sign[axis_key] for zv in self.zero_vals
            ]
            self.layout[axis_key_labels]["ticktext"] = self.labels
            self.layout[axis_key_labels]["tickmode"] = "array"

        self.layout[axis_key].update(axis_defaults)

        return self.layout[axis_key]

    def set_figure_layout(self, width, height):
        """
        Sets and returns default layout object for dendrogram figure.

        """
        self.layout.update(
            {
                "showlegend": False,
                "autosize": False,
                "hovermode": "closest",
                "width": width,
                "height": height,
            }
        )

        self.set_axis_layout(self.xaxis)
        self.set_axis_layout(self.yaxis)

        return self.layout

    def get_dendrogram_traces(self, X, colorscale, distfun, linkagefun, hovertext, color_threshold, kwargs={}):
        """
        Calculates all the elements needed for plotting a dendrogram.

        :param (ndarray) X: Matrix of observations as array of arrays
        :param (list) colorscale: Color scale for dendrogram tree clusters
        :param (function) distfun: Function to compute the pairwise distance
                                   from the observations
        :param (function) linkagefun: Function to compute the linkage matrix
                                      from the pairwise distances
        :param (list) hovertext: List of hovertext for constituent traces of dendrogram
        :rtype (tuple): Contains all the traces in the following order:
            (a) trace_list: List of Plotly trace objects for dendrogram tree
            (b) icoord: All X points of the dendrogram tree as array of arrays
                with length 4
            (c) dcoord: All Y points of the dendrogram tree as array of arrays
                with length 4
            (d) ordered_labels: leaf labels in the order they are going to
                appear on the plot
            (e) P['leaves']: left-to-right traversal of the leaves

        """
        d = distfun(X)
        Z = linkagefun(d)
        P = sch.dendrogram(
            Z,
            orientation=self.orientation,
            labels=self.labels,
            no_plot=True,
            color_threshold=color_threshold,
            **kwargs
        )

        icoord = scp.array(P["icoord"])
        dcoord = scp.array(P["dcoord"])
        ordered_labels = scp.array(P["ivl"])
        color_list = scp.array(P["color_list"])
        colors = self.get_color_dict(colorscale)

        trace_list = []

        for i in range(len(icoord)):
            if self.orientation in ["top", "bottom"]:
                xs = icoord[i]
            else:
                xs = dcoord[i]

            if self.orientation in ["top", "bottom"]:
                ys = dcoord[i]
            else:
                ys = icoord[i]
            color_key = color_list[i]
            hovertext_label = None
            if hovertext:
                hovertext_label = hovertext[i]
            trace = dict(
                type="scatter",
                x=np.multiply(self.sign[self.xaxis], xs),
                y=np.multiply(self.sign[self.yaxis], ys),
                mode="lines",
                marker=dict(color=colors[color_key]),
                text=hovertext_label,
                hoverinfo="text",
            )

            try:
                x_index = int(self.xaxis[-1])
            except ValueError:
                x_index = ""

            try:
                y_index = int(self.yaxis[-1])
            except ValueError:
                y_index = ""

            trace["xaxis"] = "x" + x_index
            trace["yaxis"] = "y" + y_index

            trace_list.append(trace)

        return trace_list, icoord, dcoord, ordered_labels, P["leaves"]

@blueprint.route('/selected_event_and_barrier', methods=['GET', 'POST'])
def selected_event_and_barrier():
    global selected_event
    selected_event = request.args['selected_event']
    
    global selected_barrier
    selected_barrier = request.args['selBarrier']
    
    print("selected events")
    print(selected_event)
    print("selected barrier")
    print("hre am i")
    print(selected_barrier)
    return "0"

@blueprint.route('/hc_selectedEvent', methods=['GET', 'POST'])
def hc_selectedEvent():
    selected = request.args['selected_event']
    if selected == "select":
        print("no selection")
    selected_event = selected_event.split(".csv")[0] + ".json"

def getDataFile(seleEvent):
    selected = seleEvent
    if selected == "select":
        return
    selected_event = selected.split(".csv")[0] + ".json"

    event_name = selected_event.split(".json")[0]
    filename = os.path.join("data", selected_event)
    try:
        with open(filename) as blog_file:
            res = json.load(blog_file)
            results = res[event_name]["articles"]["results"]
            #new code            
            df1 = pd.json_normalize(results, max_level=1)
            df2 = pd.json_normalize(results, "concepts",  ["uri", "lang", "isDuplicate", "date", "time", "dateTime", "dateTimePub", "dataType", "sim", "url", "title", 
            "body", "image", "eventUri", "sentiment", "wgt", "relevance"], record_prefix='_', max_level=1)
            df_new = df2.groupby(['uri'], as_index = False).agg({'_label.eng': ' '.join})
            df = df1.merge(df_new, on='uri', how='left')
            df.rename(columns={"_label.eng": "all_concepts"}, inplace=True)
    except:
        print("zero")
        
    database = pd.read_csv(dbfileName, encoding='latin1')
    df = df.merge(database, on='source.uri', how='left')

    df['proScore'] = -1
    df['destination'] = ""
    df['parent'] = ""
    df['count'] = 0
    df['status'] = False
    df['dateTime'] = pd.to_datetime(df['dateTime'], format='%Y-%m-%dT%H:%M:%SZ')
    df = df.sort_values(by='dateTime', ascending=True)
    return df

@blueprint.route('/hchierarchical_clustering', methods=['GET', 'POST'])
def hchierarchical_clustering():
    df = getDataFile(selected_event)        
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(df['source.title'].values.astype('U'))
    similarity_matrix = cosine_similarity(tfidf, tfidf)
    a = np.array(similarity_matrix)
    print(a.min())
    print(a.max())
    y_labels = ['Article_' + str(i) for i in range(len(df))]
    import plotly.figure_factory._dendrogram as original_dendrogram
    original_dendrogram._Dendrogram.get_dendrogram_traces = modified_dendrogram_traces
    total_clusters = 1
    try:
        total_clusters = int(float(request.args['x']))
        total_clusters = total_clusters - 1
    except:
        total_clusters = 1
    if total_clusters < 1:
        total_clusters = 1
        
    print("number of clusters = " + str(total_clusters))
    fig = create_dendrogram2(similarity_matrix, labels=y_labels, linkagefun=lambda x: sch.linkage(x, 'complete'), distfun = partial(pdist, metric='jaccard'),
    truncate_mode="level", p=total_clusters)
    fig.update_layout(width=int(request.args['width']))
    
    fig_json = fig.to_json()
    y = json.loads(fig_json)
    print(y)
    data_json = y["data"]
    print("Dictionary")
    print(len(data_json))
    
    total_c = len(data_json)
    print(data_json)
    print(total_c)
    
    global color_ran
    color_ran  = ['red', 'blue', 'green', 'pink', 'orange', 'purple', 'yellow', 'gold', 'lime', 'maroon', 'crimson', 
    'azure', 'gray', 'white', 'navy', 'mustard', 'brown', 'magenta', 'teal', 'silver']
    
    used_clrs = []
    for i in range(len(data_json)):
        print(i)
        print(data_json[i])
        used_clrs.append(data_json[i]['marker']['color'])
        print(data_json[i]['marker']['color'])
        
    global dendro_clusters
    dendro_clusters = len(set(used_clrs))
    unique_list = list(set(used_clrs))
    
    clusters_colors = []
    
    for i in range(len(data_json)):
        selc_color = color_ran[unique_list.index(data_json[i]['marker']['color'])]
        data_json[i]['marker']['color'] = selc_color
        print(data_json[i])
        clusters_colors.append(selc_color)
    
    clusters_colors = sorted(clusters_colors,key=clusters_colors.count,reverse=True)
    clusters_colors = list(set(clusters_colors))
    color_ran = clusters_colors[::-1]
    
    y["data"] = data_json
    return y

@blueprint.route('/hcThemeRiver', methods=['GET', 'POST'])
def hcThemeRiver():
    print("hc theme river")
    global total_clusters
    df = getDataFile(selected_event)
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(df['body'].values.astype('U'))
    similarity_matrix = cosine_similarity(tfidf, tfidf)
    Z = linkage(similarity_matrix, 'average')
    total_clusters = dendro_clusters #int(float(request.args['x']))
    print("number of clusters " + str(dendro_clusters))
    # n = 5
    #if total_clusters > 10:
    #    return
    clusters = cut_tree(Z, n_clusters=total_clusters)
    values = []
    for i in range(len(df)):
        values.append(clusters[i][0])
    df['cluster'] = values
    y_labels = ['Article_' + str(i) for i in range(len(df))]
    traces   = []
    clusters = []
    nc1 = pd.DataFrame()
    traces = []
           
    nc2 = pd.DataFrame()
    
    colors_list  = {}
    colors_list2 = {}
    for ind in range(total_clusters):
        colors_list["Discussion " + str(ind)]  = 0
        colors_list2["Discussion " + str(ind)] = 0
    
    
    for ind in range(total_clusters):
        if ind > -1:
            nc1 = pd.DataFrame()
            ndf = df.groupby('dateTime')['dateTime'].count()
            ndf = ndf.reset_index(name='counts')
            clus1 = df[df["cluster"] == ind]
            
            colors_list["Discussion " + str(ind)] = len(clus1)
            
            nc1 = clus1.groupby('dateTime')['dateTime'].count()
            nc1 = nc1.reset_index(name='counts')
            nc1["cluster"] = "Discussion " + str(ind)
            nc1 = pd.concat([nc1, ndf], ignore_index=True)
            nc1 = nc1.drop_duplicates(subset=['dateTime'], keep='first')
            inde = [index for index, row in nc1.iterrows() if row.isnull().any()]
            nc1.loc[inde, "cluster"] = "Discussion " + str(ind)
            nc1.loc[inde, "counts"] = 0
            #nc2 = nc2.append(nc1, ignore_index=True)
            nc2 = pd.concat([nc2, nc1])

    print(df['dateTime'][0])
    colors_list = sorted(colors_list, key=colors_list.get, reverse=True)
    colorCount = 0
    nc2["ran_col"] = "red"
    for name in colors_list:
        nc2.loc[nc2["cluster"] == colors_list[colorCount], "ran_col"] = color_ran[colorCount]
        colorCount = colorCount + 1

    for ind in range(total_clusters):
        if ind > -1:
            nc1 = pd.DataFrame()
            ndf = df.groupby('dateTime')['dateTime'].count()
            ndf = ndf.reset_index(name='counts')
            clus1 = df[df["cluster"] == ind]
     
            colors_list2["Discussion " + str(ind)] = len(clus1)
    colors_list2 = sorted(colors_list2, key=colors_list2.get, reverse=True)

    global clustered_dataframes
    clustered_dataframes = df
    
    nc2.rename(columns = {'counts':'Accumulative count'}, inplace = True)

    figure = px.area(nc2, x="dateTime", y="Accumulative count", color="cluster", line_group="cluster", line_shape='spline',color_discrete_map=dict(zip(nc2['cluster'], nc2['ran_col'])))
    figure.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    graphJSON = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@blueprint.route('/hc_word_clouds', methods=['GET', 'POST'])
def hc_word_clouds():
    print(request.args)
    check = request.args['count']
    date = request.args['date']
    cluster_no = request.args['legendgroup']
    selected = selected_event

    if selected == "select":
        print("no selection")
        return
    selected_event = selected.split(".csv")[0] + ".json"
    event_name = selected_event.split(".json")[0]
    print(selected_event)
    print(event_name)
    filename = os.path.join("data", selected_event)
    print(filename)

    with open(filename) as blog_file:
        print(filename)
        res = json.load(blog_file)
        results = res[event_name]["articles"]["results"]
        print(len(results))
        df = pd.json_normalize(results)
        print(len(df))

    database = pd.read_csv(dbfileName, encoding='latin1')
    df = df.merge(database, on='source.uri', how='left')
    df['index_col'] = df.index
    df['body_Clean_List'] = list(map(text_preprocessing, df.body))


    df['body_Clean'] = list(map(to_string, df['body_Clean_List']))
    stopwords_list = stopwords.words('english')
    stopwords_list.extend(['park', 'disney', 'disneyland'])
    df['body_Clean_List'] = [[word for word in line if word not in stopwords_list] for line in df['body_Clean_List']]
    df['body_Clean'] = list(map(to_string, df['body_Clean_List']))
    
    id2word = gensim.corpora.Dictionary(df['body_Clean_List'])
    corpus = [id2word.doc2bow(text) for text in df['body_Clean_List']]
    
    n_topics = 4


    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=n_topics, random_state=100,
                                           update_every=1, chunksize=10, passes=10, alpha='symmetric', iterations=100, per_word_topics=True)
    
    for idx, topic in lda_model.print_topics(-1):
        print("Topic: {} Word: {}".format(idx, topic))

@blueprint.route('/qaline', methods=['GET', 'POST'])
def qaline():
    print(request.args)
    sel_event = selected_event
    city_news = request.args['commaValues']
    print(city_news)
    sel_barrier = request.args["selBarrier"]
    print(sel_barrier)
    graphJSON = qacreate_bar_plot(city_news, sel_event, sel_barrier)
    return graphJSON
    return 0

def getBarrierString(sel_barrier):
    barrier = ""
    if sel_barrier == "Linguistic":
        barrier = "lang"
    elif sel_barrier == "Cultural":
        barrier = "Cultural-Class"
    elif sel_barrier == "Political":
        barrier = "Political-Alignment"
    elif sel_barrier == "Geographical":
        barrier = "country"
    elif sel_barrier == "Economic":
        barrier = "Economic-Class"
    elif sel_barrier == "Continent":
        barrier = "Continent"
    elif sel_barrier == "Religions":
        barrier = "Religions"
    elif sel_barrier == "economicbloc":
        barrier = "economicblocs"
    elif sel_barrier == "militarydefensebloc":
        barrier = "militarydefenseblocs"  
    elif sel_barrier == "politicalregionalbloc":
        barrier = "politicalregionalblocs"
    elif sel_barrier == "linguisticbloc":
        barrier = "linguisticblocs"
        
    elif sel_barrier == "SafetyandSecurity":
        barrier = "SafetyandSecurity"
    elif sel_barrier == "PersonalFreedom":
        barrier = "PersonalFreedom"
    elif sel_barrier == "Governance":
        barrier = "Governance"
    elif sel_barrier == "SocialCapital":
        barrier = "SocialCapital"
    elif sel_barrier == "InvestmentEnvironment":
        barrier = "InvestmentEnvironment"   
    elif sel_barrier == "EnterpriseConditions":
        barrier = "EnterpriseConditions"
    elif sel_barrier == "MarketAccessandInfrastructure":
        barrier = "MarketAccessandInfrastructure"
    elif sel_barrier == "EconomicQuality":
        barrier = "EconomicQuality"
    elif sel_barrier == "LivingConditions":
        barrier = "LivingConditions"
    elif sel_barrier == "Health":
        barrier = "Health"
    elif sel_barrier == "Education":
        barrier = "Education"
    elif sel_barrier == "NaturalEnvironment":
        barrier = "NaturalEnvironment"
    elif sel_barrier == "PowerDistance":
        barrier = "PowerDistance"
    elif sel_barrier == "individualism":
        barrier = "Individualism"
    elif sel_barrier == "unscertainty":
        barrier = "UncertaintyAvoidance"
    elif sel_barrier == "masculinity":
        barrier = "Masculinity"
    elif sel_barrier == "longterm":
        barrier = "LongTermOrientation"    
    elif sel_barrier == "indulgence":
        barrier = "Indulgence"
    return barrier

def qacreate_bar_plot(city_news, sel_event, sel_barrier):
    languages2 = city_news.split(',')
    plot_data = []
    df = getDataFile(sel_event)
    for col in df.columns:
        print(col)
    df['year']  = pd.DatetimeIndex(df['dateTime']).year
    df['month'] = pd.DatetimeIndex(df['dateTime']).month
    df['day']   = pd.DatetimeIndex(df['dateTime']).day
    df['date']  = pd.DatetimeIndex(df['dateTime']).date
    df['min']   = pd.DatetimeIndex(df['dateTime']).minute
    df['dateTime'] = df['dateTime'].astype('datetime64[ns]')
    df['hour']  = pd.DatetimeIndex(df['dateTime']).hour
    df['MD'] = df['dateTime'].dt.strftime('%Y-%m-%d')

    #bnb = df.groupby(["lang", "day"]).count().reset_index()
    barrier = ""
    barrier = getBarrierString(sel_barrier)
            
    print(barrier)
    nc2 = pd.DataFrame()
    nc3 = pd.DataFrame()
    
    languages = []
    for ind in range(len(languages2)):
        df3 = df[df[barrier] == languages2[ind]]
        if len(df3) > 0:
            df3.to_csv('/home/adbuls/visualisation/PropagationNetwork/flaskProject2/app/graphs/static/'+str(ind)+'.csv')
            languages.append(languages2[ind])
    
    print(df['dateTime'].min())
    print(df['dateTime'].max())
    
    print(df['dateTime'].max() - df['dateTime'].min())
    tim = df['dateTime'].max() - df['dateTime'].min()
    print(tim.days)
    
    nc2 = pd.DataFrame()
    x_label = ""
    if(tim.days > 1):
        for ind in range(len(languages)):
            if ind > -1:
                nc1 = pd.DataFrame()
                ndf = df.groupby('MD')['MD'].count()
                ndf = ndf.reset_index(name='counts')
                clus1 = df[df[barrier] == languages[ind]]
                nc1 = clus1.groupby('MD')['MD'].count()
                nc1 = nc1.reset_index(name='counts')
                nc1[barrier] = languages[ind]
                nc1 = pd.concat([nc1, ndf], ignore_index=True)
                nc1 = nc1.drop_duplicates(subset=['MD'], keep='first')
                inde = [index for index, row in nc1.iterrows() if row.isnull().any()]
                nc1.loc[inde, barrier] = languages[ind]
                nc1.loc[inde, "counts"] = 0
                nc2 = pd.concat([nc2, nc1])
        x_label = "time"
        nc2.rename(columns = {'counts':'Accumulative_count_1', 'MD': x_label}, inplace = True)
        nc3[['Accumulative_count_1', x_label, barrier]] = nc2[['Accumulative_count_1', x_label, barrier]]   #.to_numpy()
    else:
        for ind in range(len(languages)):
            if ind > -1:
                nc1 = pd.DataFrame()
                ndf = df.groupby('hour')['hour'].count()
                ndf = ndf.reset_index(name='counts')
                clus1 = df[df[barrier] == languages[ind]]
                nc1 = clus1.groupby('hour')['hour'].count()
                nc1 = nc1.reset_index(name='counts')
                nc1[barrier] = languages[ind]
                nc1 = pd.concat([nc1, ndf], ignore_index=True)
                nc1 = nc1.drop_duplicates(subset=['hour'], keep='first')
                inde = [index for index, row in nc1.iterrows() if row.isnull().any()]
                nc1.loc[inde, barrier] = languages[ind]
                nc1.loc[inde, "counts"] = 0
                nc2 = nc2.append(nc1)
        x_label = "time (hours)"
        nc2.rename(columns = {'counts':'Accumulative_count_1', 'hour':x_label}, inplace = True) 
        nc3[['Accumulative_count_1', x_label, barrier]] = nc2[['Accumulative_count_1', x_label, barrier]]   #.to_numpy()
    
    color_list = ['red', 'blue', 'green', 'pink', 'orange', 'purple', 'yellow', 'gold', 'lime', 'maroon', 'crimson', 
    'azure', 'gray', 'white', 'navy', 'mustard', 'brown', 'magenta', 'teal', 'silver']
    colors = ["blue", "azure", "bisque", "black",
                "brown", "burlywood", "chartreuse", "chocolate", "coral", "cornsilk", "crimson", "darkblue", "darkcyan", "darkgoldenrod", "darkgray", "darkgreen",
                "darkkhaki", "darkmagenta", "darkolivegreen", "darkorange", "darkorchid", "darkred", "darksalmon", "darkseagreen",
                "darkslateblue", "darkslategray", "darkslategrey", "darkturquoise", "darkviolet", "deeppink", "deepskyblue",
                "dimgray", "dodgerblue", "firebrick", "floralwhite", "forestgreen", "fuchsia", "gainsboro",
                "ghostwhite", "gold", "goldenrod", "gray", "green", "greenyellow", "honeydew", "hotpink", "indianred",
                "indigo", "ivory", "khaki", "lavender", "lavenderblush", "lawngreen", "lemonchiffon", "lightblue", "lightcoral", 
                "lightcyan", "lightgoldenrodyellow", "lightgray", "lightgreen", "lightpink", "lightsalmon", 
                "lightseagreen", "lightskyblue", "lightslategray", "lightsteelblue", "lightyellow", "lime",
                "limegreen", "linen", "magenta", "maroon", "mediumaquamarine", "mediumblue", "mediumorchid", "mediumpurple",
                "mediumseagreen", "mediumslateblue", "mediumspringgreen", "mediumturquoise", "mediumvioletred", "midnightblue",
                "mintcream", "mistyrose", "moccasin", "navajowhite", "navy", "oldlace", "olive", "olivedrab", "orange", 
                "orangered", "orchid", "palegoldenrod", "palegreen", "paleturquoise", "palevioletred", "papayawhip", "peachpuff",
                "peru", "pink", "plum", "powderblue", "purple", "red", "rosybrown", "royalblue", "rebeccapurple", "saddlebrown",
                "salmon", "sandybrown", "seagreen", "seashell", "sienna", "silver", "skyblue", "slateblue", "slategray",
                "slategrey", "snow", "springgreen", "steelblue", "tan", "teal", "thistle", "tomato", "turquoise", "violet",
                "wheat", "white", "yellow"]
                       
                
    figure = px.area(nc3, x=x_label, y="Accumulative_count_1", color = barrier, line_group = barrier, line_shape='spline', color_discrete_sequence=colors)
    
    figure.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
       
    
    figure.update_layout(
        title="", yaxis_title="Accumulative_count_1", xaxis_title="time",
             autosize=True)
    
    print(df['dateTime'][0])
    graphJSON = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@blueprint.route('/discussion_word_clouds3', methods=['GET', 'POST'])
def discussion_word_clouds3():    
    plot_data = []
    global total_clusters
    total_clusters = dendro_clusters
    
    languages = []
    for ind in range(total_clusters):
        languages.append("Discussion_"+str(ind))
    
    rows = len(languages)
    cols = 1
    subplot_titles = [l[0] for l in languages]
    
    print(clustered_dataframes)
    tot_rows = 0
    for ind in range(len(languages)):
        if ind > -1:
            clus1 = clustered_dataframes[clustered_dataframes["cluster"] == ind]
            if len(clus1)>0:
                row = ind+1 
                print(ind)
                col = 1 
                d = clus1[['dateTime', 'body']]
                d['index_col'] = d.index
                d['body_Clean_List'] = list(map(text_preprocessing, d.body))


                d['body_Clean'] = list(map(to_string, d['body_Clean_List']))
                stopwords_list = stopwords.words('english')
                stopwords_list.extend(['park', 'disney', 'disneyland'])
                d['body_Clean_List'] = [[word for word in line if word not in stopwords_list] for line in d['body_Clean_List']]
                d['body_Clean'] = list(map(to_string, d['body_Clean_List']))
    
                df_words = get_df(' '.join(d['body_Clean']))
                df_words.head(10)
                df_cn_words = [list(get_df(i)['words'][0:10]) for i in d['body_Clean']]
                df_cn_count = [list(get_df(i)['count'][0:10]) for i in d['body_Clean']]
                df_cn_content = [[i.lower()] * len(j) for i,j in zip(d['body_Clean'], df_cn_words)]

                df_cont = pd.DataFrame(zip(sum(df_cn_content,[]), sum(df_cn_words,[]),sum(df_cn_count,[])),columns = ['contents','words','count'])
    
                n = df_cont['count'].max()

                keep_dfcon = [df_cont[df_cont['contents']==i.lower()] for i in d[0:-1]]
                num_w = len(keep_dfcon)
                if num_w  > 0:
                    tot_rows = tot_rows + 1
                    
    if tot_rows > 0:
        specs = [[{'type':'xy'}] * cols] * tot_rows
        fig = sp.make_subplots(rows=tot_rows, cols=cols, specs=specs, print_grid=True, subplot_titles=languages)
        print("making figures")
        count = 0

        
        for ind in range(len(languages)):
            if ind > -1:
                nc1 = pd.DataFrame()
                row = ind+1
                print(ind)
                clus1 = clustered_dataframes[clustered_dataframes["cluster"] == ind]
                if len(clus1)>0:
                    print(ind)
                    col = 1
                    d = clus1[['dateTime', 'body']]
                    d['index_col'] = d.index
                    d['body_Clean_List'] = list(map(text_preprocessing, d.body))

                    # Return to string with to_string function
                    d['body_Clean'] = list(map(to_string, d['body_Clean_List']))
                    stopwords_list = stopwords.words('english')
                    stopwords_list.extend(['park', 'disney', 'disneyland'])
                    d['body_Clean_List'] = [[word for word in line if word not in stopwords_list] for line in d['body_Clean_List']]
                    d['body_Clean'] = list(map(to_string, d['body_Clean_List']))
    
                    df_words = get_df(' '.join(d['body_Clean']))
                    df_words.head(10)
                    df_cn_words = [list(get_df(i)['words'][0:10]) for i in d['body_Clean']]
                    
                    
                    df_cn_count = [list(get_df(i)['count'][0:10]) for i in d['body_Clean']]
                    df_cn_content = [[i.lower()] * len(j) for i,j in zip(d['body_Clean'], df_cn_words)]
            
                    df_cont = pd.DataFrame(zip(sum(df_cn_content,[]), sum(df_cn_words,[]),sum(df_cn_count,[])),columns = ['contents','words','count'])
             
                    n = df_cont['count'].max()
                    df_cont.head(10)
                    
                    keep_dfcon = [df_cont[df_cont['contents']==i.lower()] for i in d[0:-1]]
                    num_w = len(keep_dfcon)
                    
                    if num_w > 1:
                        row = ind+1
                        count = count + 1
                        n = 10
                        wordCloudStr = ' '.join(d['body_Clean'])
                        

                        figure1 = plotly_wordcloud(wordCloudStr, languages[ind])
                        
                        for trace in range(len(figure1["data"])):
                            fig.append_trace(figure1["data"][trace], row = row, col= 1)
                            fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                            fig.update_yaxes(visible=False)
                            fig.update_xaxes(visible=False)
                            fig.update_yaxes(showticklabels=False)
                            fig.update_yaxes(visible=False, showticklabels=False)
                            fig.update_layout(yaxis={'visible': False, 'showticklabels': False})
                            fig.update_layout(yaxis_visible=False, yaxis_showticklabels=False)
                            
    
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        with open("/home/adbuls/visualisation/PropagationNetwork/flaskProject2/app/graphs/static/wordclouds/sample.json", "w") as outfile:
             outfile.write(graphJSON)
        print(graphJSON)
        return graphJSON
    else:
        return json.dumps("")

@blueprint.route('/discussion_word_clouds2', methods=['GET', 'POST'])
def discussion_word_clouds2():    
    plot_data = []
    
    global total_clusters
    total_clusters = dendro_clusters
    
    languages = []
    for ind in range(total_clusters):
        languages.append("Discussion_"+str(ind))
        
    nc2 = pd.DataFrame()
    rows = len(languages)#int(len(languages)/2)
    cols = 1#2
    subplot_titles = [l[0] for l in languages]
    
    tot_rows = 0
    for ind in range(len(languages)):
        if ind > -1:
            clus1 = clustered_dataframes[clustered_dataframes["cluster"] == ind]
            if len(clus1)>0:
                row = ind+1
                print(ind)
                col = 1 
                d = clus1[['dateTime', 'body']]
                d['index_col'] = d.index
                d['body_Clean_List'] = list(map(text_preprocessing, d.body))


                d['body_Clean'] = list(map(to_string, d['body_Clean_List']))
                stopwords_list = stopwords.words('english')
                stopwords_list.extend(['park', 'disney', 'disneyland'])
                d['body_Clean_List'] = [[word for word in line if word not in stopwords_list] for line in d['body_Clean_List']]
                d['body_Clean'] = list(map(to_string, d['body_Clean_List']))
    
                df_words = get_df(' '.join(d['body_Clean']))
                df_words.head(10)
                df_cn_words = [list(get_df(i)['words'][0:10]) for i in d['body_Clean']]
                df_cn_count = [list(get_df(i)['count'][0:10]) for i in d['body_Clean']]
                df_cn_content = [[i.lower()] * len(j) for i,j in zip(d['body_Clean'], df_cn_words)]

                df_cont = pd.DataFrame(zip(sum(df_cn_content,[]), sum(df_cn_words,[]),sum(df_cn_count,[])),columns = ['contents','words','count'])
    
                n = df_cont['count'].max()
                
                keep_dfcon = [df_cont[df_cont['contents']==i.lower()] for i in d[0:-1]]
                num_w = len(keep_dfcon)
                if num_w  > 0:
                    tot_rows = tot_rows + 1
    row = 0                
    if tot_rows > 0:
        specsa = [[{'type':'xy'}] * cols] * tot_rows
        fig_Array = []#sp.make_subplots(rows=tot_rows, cols=cols, specs = specsa, print_grid=True, subplot_titles=languages)
        print("making figures")
        count = 0
        for ind in range(len(languages)):
            if ind > -1:
                nc1 = pd.DataFrame()
                clus1 = clustered_dataframes[clustered_dataframes["cluster"] == ind]
                #ndf = ndf.reset_index(name='counts')
                #clus1 = df[df[barrier] == languages[ind]]
                
                model = BERTopic()
                
                if len(clus1)>0:
                    col = 1
                    d = clus1[['dateTime', 'body']]
                    d['index_col'] = d.index
                    d['body_Clean_List'] = list(map(text_preprocessing, d.body))
                    stopwords_list = stopwords.words('english')
                    stopwords_list.extend(['park', 'disney', 'disneyland'])
                    d['body_Clean_List'] = [[word for word in line if word not in stopwords_list] for line in d['body_Clean_List']]
                    d['body_Clean'] = list(map(to_string, d['body_Clean_List']))
                    if len(d['body_Clean']) > 10:
                        docs = d.body_Clean.to_list()
                        topics, probs = model.fit_transform(docs)
                        print("print probabilities")
                        print(probs)
                        
                        top_n_topics = 4
                        freq_df = model.get_topic_freq()
                        freq_df = freq_df.loc[freq_df.Topic != -1, :]
                        topi = []
                        if topi is not None:
                            topi = list(topics)
                        elif top_n_topics is not None:
                            topi = sorted(freq_df.Topic.to_list()[:top_n_topics])
                        else:
                            topi = sorted(freq_df.Topic.to_list()[0:6])
                        print("number of bert topics")
                        print(len(topi))
                        print(topi)
                        indexes = set(topi)
                        print(indexes)
                        #time.sleep(5)            
                        tmpDict = {}
                        toc = topi.count(-1)
                        print(toc)
                        if  toc>=4:
                            row = row+1
                            count = count + 1
                            tit = "<b>Scores of topic words " + languages[ind] + "</b>"
                            
                            figure1 = model.visualize_barchart(top_n_topics = len(indexes), n_words = 7, topics = indexes, title= tit)
                            #visualize_term_rank()
                            #visualize_barchart(topics=topics, top_n_topics=4, n_words=5)
                            figure1.write_html("/home/adbuls/visualisation/PropagationNetwork/flaskProject2/app/graphs/static/abc.html")
                            
                            #print(figure1)
                            #print(type(figure1))
                            #print("the now number is")
                            #print(row)
                            #for trace in range(len(figure1["data"])):
                            #    fig_Array.add_trace(figure1["data"][trace], row = row, col= 1)
                            fig_Array.append(figure1)
        graphJSON = json.dumps(fig_Array, cls=plotly.utils.PlotlyJSONEncoder)
        with open("/home/adbuls/visualisation/PropagationNetwork/flaskProject2/app/graphs/static/wordclouds/sample.json", "w") as outfile:
             outfile.write(graphJSON)
        #print(graphJSON)
    #sleep(2)
        return graphJSON
    else:
        return json.dumps("")        

@blueprint.route('/qa_word_clouds2', methods=['GET', 'POST'])
def qa_word_clouds2():
    sel_event = selected_event
    city_news = request.args['commaValues']
    sel_barrier = request.args["selBarrier"]
    languages2 = city_news.split(',')
    
    plot_data = []
    #print(sel_barrier)
    df = getDataFile(sel_event)
    df['year'] = pd.DatetimeIndex(df['dateTime']).year
    df['month'] = pd.DatetimeIndex(df['dateTime']).month
    df['day'] = pd.DatetimeIndex(df['dateTime']).day
    df['date'] = pd.DatetimeIndex(df['dateTime']).date

    bnb = df.groupby(["lang", "day"]).count().reset_index()

    barrier = ""
    barrier = getBarrierString(sel_barrier)
    print(barrier)
    
    languages = []
    for ind in range(len(languages2)):
        df3 = df[df[barrier] == languages2[ind]]
        if len(df3) > 0:
            languages.append(languages2[ind])
    
    nc2 = pd.DataFrame()
    rows = len(languages)#int(len(languages)/2)
    cols = 1#2
    subplot_titles = [l[0] for l in languages]
    
    tot_rows = 0
    for ind in range(len(languages)):
        if ind > -1:
            nc1 = pd.DataFrame()
            print(ind)
            print(barrier)
            ndf = df.groupby('dateTime')['dateTime'].count()
            ndf = ndf.reset_index(name='counts')
            print(ind)
            print(barrier)
            clus1 = df[df[barrier] == languages[ind]]
            if len(clus1)>0:
                row = ind+1 #math.floor(ind/2)+1
                print(ind)
                col = 1 #(ind%2)+1
            #print(lst)
                d = clus1[['dateTime', 'body', barrier]]
                d['index_col'] = d.index
                d['body_Clean_List'] = list(map(text_preprocessing, d.body))

            # Return to string with to_string function
                d['body_Clean'] = list(map(to_string, d['body_Clean_List']))
                stopwords_list = stopwords.words('english')
                stopwords_list.extend(['park', 'disney', 'disneyland'])
                d['body_Clean_List'] = [[word for word in line if word not in stopwords_list] for line in d['body_Clean_List']]
                d['body_Clean'] = list(map(to_string, d['body_Clean_List']))
    
                df_words = get_df(' '.join(d['body_Clean']))
                df_words.head(10)
                df_cn_words = [list(get_df(i)['words'][0:10]) for i in d['body_Clean']]
                df_cn_count = [list(get_df(i)['count'][0:10]) for i in d['body_Clean']]
                df_cn_content = [[i.lower()] * len(j) for i,j in zip(d['body_Clean'], df_cn_words)]

                df_cont = pd.DataFrame(zip(sum(df_cn_content,[]), sum(df_cn_words,[]),sum(df_cn_count,[])),columns = ['contents','words','count'])
    
                n = df_cont['count'].max()
                
            #color_dict = get_colordict('viridis',n , 1)

            #create a list contains DataFrame of each content
                keep_dfcon = [df_cont[df_cont['contents']==i.lower()] for i in d[0:-1]]
                num_w = len(keep_dfcon)
                if num_w  > 0:
                    tot_rows = tot_rows + 1
    row = 0                
    if tot_rows > 0:
        specsa = [[{'type':'xy'}] * cols] * tot_rows
        fig_Array = []#sp.make_subplots(rows=tot_rows, cols=cols, specs = specsa, print_grid=True, subplot_titles=languages)
        print("making figures")
        count = 0
        for ind in range(len(languages)):
            if ind > -1:
                nc1 = pd.DataFrame()
                ndf = df.groupby('dateTime')['dateTime'].count()
                ndf = ndf.reset_index(name='counts')
                clus1 = df[df[barrier] == languages[ind]]
                
                model = BERTopic()
                
                if len(clus1)>0:
                    col = 1
                    d = clus1[['dateTime', 'body', barrier]]
                    d['index_col'] = d.index
                    d['body_Clean_List'] = list(map(text_preprocessing, d.body))
                    stopwords_list = stopwords.words('english')
                    stopwords_list.extend(['park', 'disney', 'disneyland'])
                    d['body_Clean_List'] = [[word for word in line if word not in stopwords_list] for line in d['body_Clean_List']]
                    d['body_Clean'] = list(map(to_string, d['body_Clean_List']))
                    if len(d['body_Clean']) > 10:
                        docs = d.body_Clean.to_list()
                        topics, probs = model.fit_transform(docs)
                        print("print probabilities")
                        print(probs)
                        
                        top_n_topics = 4
                        freq_df = model.get_topic_freq()
                        freq_df = freq_df.loc[freq_df.Topic != -1, :]
                        topi = []
                        if topi is not None:
                            topi = list(topics)
                        elif top_n_topics is not None:
                            topi = sorted(freq_df.Topic.to_list()[:top_n_topics])
                        else:
                            topi = sorted(freq_df.Topic.to_list()[0:6])
                        print("number of bert topics")
                        print(len(topi))
                        print(topi)
                        indexes = set(topi)
                        print(indexes)
                        #time.sleep(5)            
                        tmpDict = {}
                        toc = topi.count(-1)
                        print(toc)
                        if  toc>=4:
                            row = row+1
                            count = count + 1
                            tit = "<b>Topic Word Scores " + languages[ind] + "</b>"
                            
                            figure1 = model.visualize_barchart(top_n_topics = len(indexes), n_words = 10, topics = indexes, title= tit)
                            #visualize_term_rank()
                            #visualize_barchart(topics=topics, top_n_topics=4, n_words=5)
                            figure1.write_html("/home/adbuls/visualisation/PropagationNetwork/flaskProject2/app/graphs/static/abc.html")
                            
                            #print(figure1)
                            #print(type(figure1))
                            #print("the now number is")
                            #print(row)
                            #for trace in range(len(figure1["data"])):
                            #    fig_Array.add_trace(figure1["data"][trace], row = row, col= 1)
                            fig_Array.append(figure1)
        graphJSON = json.dumps(fig_Array, cls=plotly.utils.PlotlyJSONEncoder)
        with open("/home/adbuls/visualisation/PropagationNetwork/flaskProject2/app/graphs/static/wordclouds/sample.json", "w") as outfile:
             outfile.write(graphJSON)
        #print(graphJSON)
    #sleep(2)
        return graphJSON
    else:
        return json.dumps("")
    
    
@blueprint.route('/qa_word_clouds5', methods=['GET', 'POST'])
def qa_word_clouds5():
    print(request.args)
    check = request.args['count']
    dateTime = request.args['date']
    cluster_no = request.args['legendgroup']
    selected = selected_event

    df = getDataFile(selected_event)
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(df['source.title'].values.astype('U'))
    similarity_matrix = cosine_similarity(tfidf, tfidf)
    Z = linkage(similarity_matrix, 'ward')

    clusters = cut_tree(Z, n_clusters=dendro_clusters)
    values = []
    for i in range(len(df)):
        values.append("Discussion " + str(clusters[i][0]))
    df['cluster'] = values

    nc1 = pd.DataFrame()
    traces = []
    color_list = ['red', 'blue', 'green', 'pink', 'orange', 'purple', 'yellow', 'gold', 'lightcoral', 'darkorange']

    print(check)
    print(dateTime)
    print(cluster_no)
    print(df.columns)
    print(len(df))

    df['dateTime'] = pd.to_datetime(df['dateTime'], format='%Y-%m-%d %H:%M:%S')
    df = df.sort_values(by='dateTime', ascending=True)
    df['year'] = pd.DatetimeIndex(df['dateTime']).year
    df['month'] = pd.DatetimeIndex(df['dateTime']).month
    df['day'] = pd.DatetimeIndex(df['dateTime']).day
    df['date'] = pd.DatetimeIndex(df['dateTime']).date
    
    #df = df[['dateTime', 'title', 'cluster']]
    df = df[df["cluster"] == cluster_no]
    selected_cluster = df[df["dateTime"] == dateTime]
    selected_cluster = selected_cluster[['dateTime', 'body', 'cluster']]
    
    selected_cluster['index_col'] = selected_cluster.index
    selected_cluster['body_Clean_List'] = list(map(text_preprocessing, selected_cluster.body))

    # Return to string with to_string function
    selected_cluster['body_Clean'] = list(map(to_string, selected_cluster['body_Clean_List']))
    stopwords_list = stopwords.words('english')
    stopwords_list.extend(['park', 'disney', 'disneyland'])
    selected_cluster['body_Clean_List'] = [[word for word in line if word not in stopwords_list] for line in selected_cluster['body_Clean_List']]
    selected_cluster['body_Clean'] = list(map(to_string, selected_cluster['body_Clean_List']))
    
    
    df_words = get_df(' '.join(selected_cluster['body_Clean']))
    df_words.head(10)
    df_cn_words = [list(get_df(i)['words'][0:10]) for i in selected_cluster['body_Clean']]
    df_cn_count = [list(get_df(i)['count'][0:10]) for i in selected_cluster['body_Clean']]
    df_cn_content = [[i.lower()] * len(j) for i,j in zip(selected_cluster['body_Clean'], df_cn_words)]

    df_cont = pd.DataFrame(zip(sum(df_cn_content,[]), sum(df_cn_words,[]),sum(df_cn_count,[])), columns = ['contents','words','count'])
    
    print(df_cont)
    n = df_cont['count'].max()
    keep_dfcon = [df_cont[df_cont['contents']==i.lower()] for i in selected_cluster[0:-1]]
    num_w = len(keep_dfcon)
    count = 0
    if num_w  > 1:
        specs = [[{'type':'xy'}] * 1] * 1
        fig = sp.make_subplots(rows=1, cols=1, specs=specs, print_grid=True, subplot_titles=[dateTime])
        count = count + 1
        n = 10
        wordCloudStr = ' '.join(selected_cluster['body_Clean'])
        figure1 = plotly_wordcloud(wordCloudStr, cluster_no)
        for trace in range(len(figure1["data"])):
            fig.append_trace(figure1["data"][trace], row = 1, col= 1)
            fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
            fig.update_yaxes(visible=False)
            fig.update_xaxes(visible=False)
            fig.update_yaxes(showticklabels=False)
            fig.update_yaxes(visible=False, showticklabels=False)
            fig.update_layout(yaxis={'visible': False, 'showticklabels': False})
            fig.update_layout(yaxis_visible=False, yaxis_showticklabels=False)
                            
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        with open("/home/adbuls/visualisation/PropagationNetwork/flaskProject2/app/graphs/static/wordclouds/sample.json", "w") as outfile:
             outfile.write(graphJSON)
        print(graphJSON)
    #sleep(2)
        return graphJSON
    else:
        return json.dumps("")

@blueprint.route('/qa_analysis_table', methods=['GET', 'POST'])
def qa_analysis_table():
    print(request.args)
    check = request.args['count']
    dateTime = request.args['date']
    cluster_no = request.args['legendgroup']
    selected = selected_event
    sel_barrier = request.args['selBarrier']
    df = getDataFile(sel_event)
    df['year'] = pd.DatetimeIndex(df['dateTime']).year
    df['month'] = pd.DatetimeIndex(df['dateTime']).month
    df['day'] = pd.DatetimeIndex(df['dateTime']).day
    df['date'] = pd.DatetimeIndex(df['dateTime']).date

    bnb = df.groupby(["lang", "day"]).count().reset_index()

    barrier = ""
    barrier = getBarrierString(sel_barrier)
    color_list = ['red', 'blue', 'green', 'pink', 'orange', 'purple', 'yellow', 'gold', 'lightcoral', 'darkorange']
    
    
    df['dateTime'] = pd.to_datetime(df['dateTime'], format='%Y-%m-%dT%H:%M:%SZ')
    df = df[df[barrier] == cluster_no]
    selected_cluster = df[df["dateTime"] == dateTime]
    selected_cluster = selected_cluster[['dateTime', 'title', barrier]]
    
    print("length is")
    print(len(selected_cluster))
    print(selected_cluster)
    print(len(selected_cluster))
    
    class ItemTable(Table):
        date = Col('date')
        time = Col('time')
        title = LinkCol('Title', 'graphs_blueprint.get_doc_display', url_kwargs=dict(news_site='news_site', rank='rank'), attr='title')
        cluster = Col('cluster')
        country = Col('country')

    class Item(object):
        def __init__(self, date, time, title, cluster, country):
            self.date = date
            self.time = time
            self.title = title
            self.cluster = cluster
            self.country = country

    print(dict(values=list(selected_cluster.columns)))

    data = [go.Table(
        header=dict(values=list(selected_cluster.columns), font={"size": 20}),
        cells=dict(values=[ selected_cluster['dateTime'], selected_cluster['title'], selected_cluster[barrier]],
                   font={"size": 18})
    )]
    print(data)
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@blueprint.route('/qa_word_clouds3', methods=['GET', 'POST'])
def qa_word_clouds3():
    print(request.args)
    check = request.args['count']
    dateTime = request.args['date']
    cluster_no = request.args['legendgroup']
    selected = selected_event
    df = getDataFile(selected)
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(df['source.title'].values.astype('U'))
    similarity_matrix = cosine_similarity(tfidf, tfidf)
    Z = linkage(similarity_matrix, 'ward')

    print("number of clusters" + str(total_clusters))
    clusters = cut_tree(Z, n_clusters=dendro_clusters)
    values = []
    for i in range(len(df)):
        values.append("Cluster_" + str(clusters[i][0]))
    df['cluster'] = values

    nc1 = pd.DataFrame()
    traces = []
    color_list = ['red', 'blue', 'green', 'pink', 'orange', 'purple', 'yellow', 'gold', 'lightcoral', 'darkorange']

    print(check)
    print(dateTime)
    print(cluster_no)
    print(df.columns)
    print(len(df))


    df['dateTime'] = pd.to_datetime(df['dateTime'], format='%Y-%m-%d %H:%M:%S')
    df = df.sort_values(by='dateTime', ascending=True)
    df['year'] = pd.DatetimeIndex(df['dateTime']).year
    df['month'] = pd.DatetimeIndex(df['dateTime']).month
    df['day'] = pd.DatetimeIndex(df['dateTime']).day
    df['date'] = pd.DatetimeIndex(df['dateTime']).date
    
    df = df[df["cluster"] == cluster_no]
    selected_cluster = df[df["dateTime"] == dateTime]
    selected_cluster = selected_cluster[['dateTime', 'body', 'cluster']]
    
    selected_cluster['index_col'] = selected_cluster.index
    selected_cluster['body_Clean_List'] = list(map(text_preprocessing, selected_cluster.body))

    selected_cluster['body_Clean'] = list(map(to_string, selected_cluster['body_Clean_List']))
    stopwords_list = stopwords.words('english')
    stopwords_list.extend(['park', 'disney', 'disneyland'])
    selected_cluster['body_Clean_List'] = [[word for word in line if word not in stopwords_list] for line in selected_cluster['body_Clean_List']]
    selected_cluster['body_Clean'] = list(map(to_string, selected_cluster['body_Clean_List']))
    
    
    df_words = get_df(' '.join(selected_cluster['body_Clean']))
    df_words.head(10)
    df_cn_words = [list(get_df(i)['words'][0:10]) for i in selected_cluster['body_Clean']]
    df_cn_count = [list(get_df(i)['count'][0:10]) for i in selected_cluster['body_Clean']]
    df_cn_content = [[i.lower()] * len(j) for i,j in zip(selected_cluster['body_Clean'], df_cn_words)]

    df_cont = pd.DataFrame(zip(sum(df_cn_content,[]), sum(df_cn_words,[]),sum(df_cn_count,[])),
                       columns = ['contents','words','count'])
    
    print(df_cont)
    n = df_cont['count'].max()
    keep_dfcon = [df_cont[df_cont['contents']==i.lower()] for i in selected_cluster[0:-1]]
    num_w = len(keep_dfcon)
    n = 10
    pal = list(sns.color_palette(palette='Reds_r', n_colors=n).as_hex())

    fig = px.pie(df_words[0:10], values='count', names='words',color_discrete_sequence=pal)
    fig.update_traces(textposition='outside', textinfo='percent+label', hole=.6, hoverinfo="label+percent+name")
    fig.update_traces(title = cluster_no,title_font = dict(size=25,family='Verdana',color='darkred'),hoverinfo='label+percent',textinfo='percent', textfont_size=20)
                    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@blueprint.route('/qa_word_clouds', methods=['GET', 'POST'])
def qa_word_clouds():
    print(request.args)
    check = request.args['count']
    dateTime = request.args['date']
    cluster_no = request.args['legendgroup']
    selected = selected_event
    sel_barrier = request.args['selBarrier']
    df = getDataFile(selected)
    df['year'] = pd.DatetimeIndex(df['dateTime']).year
    df['month'] = pd.DatetimeIndex(df['dateTime']).month
    df['day'] = pd.DatetimeIndex(df['dateTime']).day
    df['date'] = pd.DatetimeIndex(df['dateTime']).date

    bnb = df.groupby(["lang", "day"]).count().reset_index()

    barrier = ""
    barrier = getBarrierString(sel_barrier)
    color_list = ['red', 'blue', 'green', 'pink', 'orange', 'purple', 'yellow', 'gold', 'lightcoral', 'darkorange']
   
    df['dateTime'] = pd.to_datetime(df['dateTime'], format='%Y-%m-%dT%H:%M:%SZ')
    df = df[df[barrier] == cluster_no]
    selected_cluster = df[df["dateTime"] == dateTime]
    selected_cluster = selected_cluster[['dateTime', 'body', barrier]]
    
    selected_cluster['index_col'] = selected_cluster.index
    selected_cluster['body_Clean_List'] = list(map(text_preprocessing, selected_cluster.body))

    # Return to string with to_string function
    selected_cluster['body_Clean'] = list(map(to_string, selected_cluster['body_Clean_List']))
    stopwords_list = stopwords.words('english')
    stopwords_list.extend(['park', 'disney', 'disneyland'])
    selected_cluster['body_Clean_List'] = [[word for word in line if word not in stopwords_list] for line in selected_cluster['body_Clean_List']]
    selected_cluster['body_Clean'] = list(map(to_string, selected_cluster['body_Clean_List']))
    
    
    df_words = get_df(' '.join(selected_cluster['body_Clean']))
    df_words.head(10)
    df_cn_words = [list(get_df(i)['words'][0:10]) for i in selected_cluster['body_Clean']]
    df_cn_count = [list(get_df(i)['count'][0:10]) for i in selected_cluster['body_Clean']]
    df_cn_content = [[i.lower()] * len(j) for i,j in zip(selected_cluster['body_Clean'], df_cn_words)]

    df_cont = pd.DataFrame(zip(sum(df_cn_content,[]), sum(df_cn_words,[]),sum(df_cn_count,[])), columns = ['contents','words','count'])
    
    print(df_cont)
    n = df_cont['count'].max()
    #color_dict = get_colordict('viridis',n , 1)

    #create a list contains DataFrame of each content
    keep_dfcon = [df_cont[df_cont['contents']==i.lower()] for i in selected_cluster[0:-1]]
    num_w = len(keep_dfcon)
    n = 10
    pal = list(sns.color_palette(palette='Reds_r', n_colors=n).as_hex())

    fig = px.pie(df_words[0:10], values='count', names='words',color_discrete_sequence=pal)

    fig.update_traces(textposition='outside', textinfo='percent+label', hole=.6, hoverinfo="label+percent+name")

    #fig.update_layout(width = 800, height = 600,
     #             margin = dict(t=0, l=0, r=0, b=0))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON       
 
def get_df(input_text):
    list_words = input_text.split(' ')
    set_words_full = list(set(list_words))
    
    #remove stop words
    set_words = [i for i in set_words_full if i not in stop_words]
    
    #count each word
    count_words = [list_words.count(i) for i in set_words]
    
    #create DataFrame
    df = pd.DataFrame(zip(set_words, count_words), columns=['words','count'])
    df.sort_values('count', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df 
        
 
def get_colordict(palette,number,start):
    pal = list(sns.color_palette(palette=palette, n_colors=number).as_hex())
    color_d = dict(enumerate(pal, start=start))
    return color_d

@blueprint.route('/getKeywords', methods=['GET', 'POST'])
def getKeywords():
    print("getEvents")
    selected = request.args['selected_event']
    return getForPropagationNetworkNew2Tree(selected)
    
@blueprint.route('/getKeywords2', methods=['GET', 'POST'])
def getKeywords2():
    print("getKeywords")
    selected = request.args['selected_event']
    cons = "_".join(selected.split() )
    PARAMS = {"action": "getEvents",
              "eventsPage": 1,
              "conceptUri": cons,
              "includeArticleConcepts": True,
              "eventsCount": 10,
              'eventsSortBy': "date",
              'eventsSortByAsc': False,
              "resultType": "events",
              "apiKey": KEY}
              
    conceptUri = "http://en.wikipedia.org/wiki/"+cons   
    print(conceptUri)
    q = QueryEventsIter(conceptUri)
    res = []
    resDic = {}
    for event in q.execQuery(er, sortBy = "rel", maxItems = 10):
        print(event)
        res.append(event)
        k  = event["uri"]
        va = event["title"]["eng"]
        print(k)
        print(va)
        resDic[k] = va
    
    print(resDic)
    print(len(res))
    #b = {selected:{"events":{"results":res}}}
    
    #json_object = json.dumps(res, indent=4)
    #with open(os.path.join("/home/adbuls/visualisation/PropagationNetwork/flaskProject2/data", selected+".json"), "w") as outfile:
    #     outfile.write(json_object)
    
    #res = open(os.path.join("/home/adbuls/visualisation/PropagationNetwork/flaskProject2/data","Pakistan.json"), "r")
    #df1 = pd.json_normalize(res, max_level=1)
    #print(list(df.columns))
    return resDic    
    

@blueprint.route('/getForPropagationNetworkNew2Tree/<string:name>', methods=['GET'])
def getForPropagationNetworkNew2Tree(name, url="http://eventregistry.org/api/v1/event/getEvent", page=1, per_page=100, articles=[]):
    PARAMS = {"action": "getEvent",
              "articlesPage": page,
              "eventUri": name,
              "includeArticleConcepts": True,
              "articlesCount": per_page,
              'articlesSortBy': "date",
              'articlesSortByAsc': False,
              "resultType": "articles",
              "apiKey": KEY}
    print(url)
    
    r = requests.get(url=url, params=PARAMS)
    res = r.json()  
    #if r.status_code == 200:
    if page <= int(res[str(name)]["articles"]["pages"]):
        results = res[str(name)]["articles"]["results"]
        #print(results)
        articles = articles + results
        print(len(articles))
        page += 1
        time.sleep(.300)
        return getForPropagationNetworkNew2Tree(name, "http://eventregistry.org/api/v1/event/getEvent", page, per_page,articles)
    
    else:

        b = {name:{"articles":{"results":articles}}}

        json_object = json.dumps(b, indent=4)
        with open(os.path.join("/home/adbuls/visualisation/PropagationNetwork/flaskProject2/data", name+".json"), "w") as outfile:
            outfile.write(json_object)

        df1 = pd.json_normalize(articles, max_level=1)
    
        df2 = pd.json_normalize(articles, "concepts",  ["uri", "lang", "isDuplicate", "date", "time", "dateTime", "dateTimePub", "dataType", "sim", "url", "title", 
        "body", "image", "eventUri", "sentiment", "wgt", "relevance"], record_prefix='_', max_level=1)
    
        df_new = df2.groupby(['uri'], as_index = False).agg({'_label.eng': ' '.join})
    
        df = df1.merge(df_new, on='uri', how='left')
    
        print(len(df1))
        print(len(df2))
        print(len(df_new))
        print(len(df))
        print(df.columns)
        print(df_new.columns)
    
        df.rename(columns={"_label.eng": "all_concepts"}, inplace=True)
        print(df.columns)
        print(df)
    
    #time.sleep(1000)
    #print(df)
        database = pd.read_csv(dbfileName, encoding='latin1')
        df = df.merge(database, on='source.uri', how='left')

        df['proScore'] = -1
        df['destination'] = ""
        df['parent'] = ""
        df['count'] = 0
        df['status'] = False
        print(len(df))
        df['dateTime'] = pd.to_datetime(df['dateTime'], format='%Y-%m-%dT%H:%M:%SZ')
        df = df.sort_values(by='dateTime', ascending=True)

    #  getForPropagationNetworkNew2Tree
        df, dateFrom, dateTo = getSimilarityTree(df)
        df.head(10)
        root = dataframe_to_tree(df, path_col="Path", attribute_cols=["dateFrom", "dateTo", "group"], )
        df = tree_to_dataframe(root, all_attrs=True)
        print(len(df))
        glo_dataframes = df
        print("the final dataframes have been created")
        print(os.getcwd())
        df.to_csv(os.path.join("/home/adbuls/visualisation/PropagationNetwork/flaskProject2/app/graphs/static/", name+".csv"))
    #df.to_csv("http://cleopatra.ijs.si/sensoranalysis/static/"+)
        return "1"

    
    
def getForPropagationNetworkNew2TreeOnlyOne(matrix, df):
    print("type of matrix")
    # print(type(matrix))
    # print(len(matrix))
    #columns = []
    #for a in range(len(matrix)):
    #    columns.append("Col_" + str(a))
    #ndf = pd.DataFrame(matrix, columns=columns)
    # print(len(ndf))

    rows, cols = np.where((matrix >= threshold))
    # print(rows)
    # print(cols)
    edges = zip(rows.tolist(), cols.tolist())
    # print(type(edges))
    # print(edges)
    gr = nx.Graph()
    gr.add_edges_from(edges)

    print("here is graph")
    # print(gr.edges())
    print("len of edges")
    print(len(gr.edges()))
    #gr.remove_edges_from(nx.selfloop_edges(gr))
    print(len(gr.edges()))
    #print(gr.edges())
    keys = df['uri'].tolist()
    nodesTree = [["Event", "", "", "0", "", "", "", "", "", "", "", ""]]
    count = 0

    for u, v in gr.edges:
        print(count)
        count += 1
        uri1 = keys[u]
        uri2 = keys[v]
        art1 = df[df["uri"] == uri1]
        art2 = df[df["uri"] == uri2]
        idx1 = df.index[df["uri"] == uri1].values[0]
        idx2 = df.index[df["uri"] == uri2].values[0]
        d1s = art1["dateTime"].tolist()
        print(d1s)
        d1 = datetime.datetime.strptime(str(d1s[0]), '%Y-%m-%d %H:%M:%S')
        d2s = art2["dateTime"].tolist()
        d2 = datetime.datetime.strptime(str(d2s[0]), '%Y-%m-%d %H:%M:%S')

        if d2 > d1:
            if df.at[idx1, 'parent'] == "":
                df.at[idx1, 'parent'] = "Event/" + str(uri1)

                nodesTree.append(["Event/" + str(uri1),
                                  str(d1).replace(" ", "T"), str(d1).replace(" ", "T"), "0", df.at[idx1, 'source.uri'], df.at[idx1, 'country'], df.at[idx1, 'lang'], df.at[idx1, 'Political-Alignment'], 
                                  df.at[idx1, 'wiki-url'], df.at[idx1, 'Cultural-Class'], df.at[idx1, 'Economic-Class'], df.at[idx1, 'Continent'], df.at[idx1, 'Religions'],df.at[idx1, 'economicblocs'], df.at[idx1, 'militarydefenseblocs'],
                                  df.at[idx1, 'politicalregionalblocs'], df.at[idx1, 'linguisticblocs'],
                                  df.at[idx1, 'SafetyandSecurity'], df.at[idx1, 'PersonalFreedom'], df.at[idx1, 'Governance'], df.at[idx1, 'SocialCapital'],
                                  df.at[idx1, 'InvestmentEnvironment'], df.at[idx1, 'EnterpriseConditions'], df.at[idx1, 'MarketAccessandInfrastructure'], df.at[idx1, 'EconomicQuality'],
                                  df.at[idx1, 'LivingConditions'], df.at[idx1, 'Health'], df.at[idx1, 'Education'], df.at[idx1, 'NaturalEnvironment'],
                                  df.at[idx1, 'PowerDistance'], df.at[idx1, 'Individualism'], df.at[idx1, 'UncertaintyAvoidance'], df.at[idx1, 'Masculinity'],
                                  df.at[idx1, 'LongTermOrientation'], df.at[idx1, 'Indulgence']
                                  ])

                df.at[idx1, 'status'] = True

            if not df.at[idx2, 'status']:
                df.at[idx2, 'parent'] = df.at[idx1, 'parent'] + "/" + str(uri2)

                color = df.at[idx1, 'parent'].split('/')

                nodesTree.append([df.at[idx1, 'parent'] + "/" + str(uri2),
                              str(d1).replace(" ", "T"), str(d2).replace(" ", "T"), color[1], df.at[idx2, 'source.uri'],
                              df.at[idx2, 'country'], df.at[idx2, 'lang'], df.at[idx2, 'Political-Alignment'],
                              df.at[idx2, 'wiki-url'], df.at[idx2, 'Cultural-Class'], 
                              df.at[idx2, 'Economic-Class'], df.at[idx2, 'Continent'], df.at[idx2, 'Religions']
                             ,df.at[idx2, 'economicblocs'], df.at[idx2, 'militarydefenseblocs'], 
                              df.at[idx2, 'politicalregionalblocs'], df.at[idx2, 'linguisticblocs'],
                              df.at[idx1, 'SafetyandSecurity'], df.at[idx1, 'PersonalFreedom'], df.at[idx1, 'Governance'], df.at[idx1, 'SocialCapital'],
                              df.at[idx1, 'InvestmentEnvironment'], df.at[idx1, 'EnterpriseConditions'], df.at[idx1, 'MarketAccessandInfrastructure'], df.at[idx1, 'EconomicQuality'],
                              df.at[idx1, 'LivingConditions'], df.at[idx1, 'Health'], df.at[idx1, 'Education'], df.at[idx1, 'NaturalEnvironment'],
                              df.at[idx1, 'PowerDistance'], df.at[idx1, 'Individualism'], df.at[idx1, 'UncertaintyAvoidance'], df.at[idx1, 'Masculinity'],
                              df.at[idx1, 'LongTermOrientation'], df.at[idx1, 'Indulgence']
                              ])

                df.at[idx2, 'status'] = True


    path_data = pd.DataFrame(nodesTree, columns=['Path', 'dateFrom', 'dateTo', 'group', 'source', 'country', 'lang',
                                                 'polalign', 'url', 'culture', 'economic', 'continent', 'religions',
                                                 'economicblocs', 'militarydefenseblocs','politicalregionalblocs',
                                                 'linguisticblocs', 'SafetyandSecurity', 'PersonalFreedom', 'Governance','SocialCapital','InvestmentEnvironment','EnterpriseConditions','MarketAccessandInfrastructure','EconomicQuality',
                                                 'LivingConditions','Health', 'Education','NaturalEnvironment','PowerDistance','Individualism','UncertaintyAvoidance','Masculinity','LongTermOrientation', 'Indulgence'],)
    # print(len(path_data))
    path_data = path_data.drop_duplicates(subset=["Path"], keep='first')
    return path_data, False, False
    

def getSimilarityTree(df):
    print("getSimilarityTree")
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(df['all_concepts'].values.astype('U'))
    #tfidf = vectorizer.fit_transform(df['body'].values.astype('U'))
    similarity_matrix = cosine_similarity(tfidf, tfidf)
    # print(type(similarity_matrix))
    return getForPropagationNetworkNew2TreeOnlyOne(similarity_matrix, df)
    # return getForPropagationNetworkNew23(similarity_matrix, df)
    # keys = df['uri'].tolist()
    # print(keys)
    # return similarity_matrix
    # return getForPropagationNetworkNew23OnlyOne(similarity_matrix, df)

@blueprint.route('/getDownloadedEvents', methods=['GET', 'POST'])
def getDownloadedEvents():
    return all_events

@blueprint.route('/getDownloadedEventsCustom', methods=['GET', 'POST'])
def getDownloadedEventsCustom():
    selected = request.args['selected_event']
    return all_events

def getWordClouds(txt):
    wordcloud2 = WordCloud().generate(txt)

def get_files(target):
    for file in os.listdir(target):
        path = os.path.join(target, file)
        if os.path.isfile(path):
            yield (
                file,
                datetime.utcfromtimestamp(os.path.getmtime(path)),
                os.path.getsize(path)
            )


def text_preprocessing(text):
    
    # Convert words to lower case
    text = text.lower()
    
    # Expand contractions
    if True:
        text = text.split()
        new_text = []
        for word in text:
            if word in contractions:
                new_text.append(contractions[word])
            else:
                new_text.append(word)
        text = " ".join(new_text)
        
    # Format words and remove unwanted characters
    text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\<a href', ' ', text)
    text = re.sub(r'&amp;', '', text) 
    text = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/]', ' ', text)
    text = re.sub(r'<br />', ' ', text)
    text = re.sub(r'\'', ' ', text) 

    # Tokenize each word
    text = nltk.WordPunctTokenizer().tokenize(text)

    # Lemmatize each word
    text = [nltk.stem.WordNetLemmatizer().lemmatize(token, pos='v') for token in text if len(token)>1]
    
    return text


def to_string(text):
    # Convert list to string
    text = ' '.join(map(str, text))

    return text
    
    
# Define a function to plot word cloud
def plot_cloud(wordcloud):
    # Set figure size
    plt.figure(figsize=(40, 30))
    # Display image
    plt.imshow(wordcloud) 
    # No axis details
    plt.axis("off");
    

def create_wordcloud(topic_model, topic):
    text = {word: value for word, value in topic_model.get_topic(topic)}
    wc = WordCloud(background_color="white", max_words=1000)
    wc.generate_from_frequencies(text)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def plotly_wordcloud(text, tit):
    wc = WordCloud(stopwords = set(STOPWORDS), max_words = 200, max_font_size = 100)
    wc.generate_from_frequencies(text)
    
    word_list=[]
    freq_list=[]
    fontsize_list=[]
    position_list=[]
    orientation_list=[]
    color_list=[]

    for (word, freq), fontsize, position, orientation, color in wc.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)
        
    # get the positions
    x=[]
    y=[]
    for i in position_list:
        x.append(i[0])
        y.append(i[1])
            
    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i*100)
    new_freq_list
    
    trace = go.Scatter(x=x, 
                       y=y, 
                       name= tit,
                       textfont = dict(size=new_freq_list, color=color_list),
                       hoverinfo='text',
                       hovertext=['{0}{1}'.format(w, f) for w, f in zip(word_list, freq_list)],
                       mode='text',  
                       text=word_list
                      )
    
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False, 'visible': True},
                        'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False, 'visible': False},
                        })
    
    fig = go.Figure(data=[trace], layout=layout)
    #fig.update_layout(legend_title=dict(text='Country', font=dict(family="sans-serif", size = 18, color='blue')))
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    fig.update_yaxes(visible=False)
    fig.update_xaxes(visible=True)
    
    fig.update_yaxes(showticklabels=False)
    fig.update_yaxes(visible=False, showticklabels=False)

    fig.update_layout(yaxis={'visible': False, 'showticklabels': False})
    fig.update_layout(yaxis_visible=False, yaxis_showticklabels=False)
    

    return fig

def ctree():
    """ One of the python gems. Making possible to have dynamic tree structure.

    """
    return defaultdict(ctree)


def build_leaf(name, leaf):
    """ Recursive function to build desired custom tree structure

    """
    res = {"name": name, "value": 123}

    # add children node if the leaf actually has any children
    if len(leaf.keys()) > 0:
        res["children"] = [build_leaf(k, v) for k, v in leaf.items()]

    return res


@blueprint.route('/generateCommunity', methods=['GET', 'POST'])
def generateCommunity():
    df = getDataFile(selected_event)
    sel_barrier = request.args['barrier']
    print(sel_barrier)
    barrier = ""
    barrier = getBarrierString(sel_barrier)
    df2 = df[['eventUri','country',barrier]]
    df2.to_csv(os.path.join("/home/adbuls/visualisation/PropagationNetwork/flaskProject2/app/graphs/static", "Radial.csv"),index=False)
    
    tree = ctree()
    # NOTE: you need to have test.csv file as neighbor to this file
    with open("/home/adbuls/visualisation/PropagationNetwork/flaskProject2/app/graphs/static/Radial.csv") as csvfile:
        reader = csv.reader(csvfile)
        for rid, row in enumerate(reader):
        
            # skipping first header row. remove this logic if your csv is
            # headerless
            if rid == 0:
                continue
            print(row)
            print(rid)
            # usage of python magic to construct dynamic tree structure and
            # basically grouping csv values under their parents
            leaf = tree[row[0]]
            for cid in range(1, len(row)):
                leaf = leaf[row[cid]]

    # building a custom tree structure
    res = []
    for name, leaf in tree.items():
        res.append(build_leaf(name, leaf))


    
    # printing results into the terminal
    treeValues = json.dumps(res)
    print(treeValues)
    jsonFilew = open("/home/adbuls/visualisation/PropagationNetwork/flaskProject2/app/graphs/static/Radial.json", "w")
    jsonFilew.write(treeValues)
    jsonFilew.close()
    with open("/home/adbuls/visualisation/PropagationNetwork/flaskProject2/app/graphs/static/Radial.json") as jsonFile:
        data = json.load(jsonFile)
        data2 = data[0];
        print(data2)
    return data2
    print(treeValues[0])
    return treeValues
    

def getNetworkForRadialTree(matrix, df):
    print("type of matrix")
    rows, cols = np.where((matrix >= 0.9))
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.Graph()
    gr.add_edges_from(edges)
    gr.remove_edges_from(nx.selfloop_edges(gr))

    values = df['uri'].tolist()
    values = list(map(int, values))
    keys   = [*range(0, len(values), 1)]
    
    mapping = dict(zip(keys, values))
    print(mapping)
    H = nx.relabel_nodes(gr, mapping)
    print(H)
    data1 = nx.node_link_data(H,  {"id": "name"})
    
    return data1 

@blueprint.route('/generateRadialTree', methods=['GET', 'POST'])
def generateRadialTree():
    df = getDataFile(selected_event)
    sel_barrier = request.args['barrier']
    print(sel_barrier)
    barrier = ""
    barrier = getBarrierString(sel_barrier)
    df = df[df[barrier].notna()]
    print("getSimilarityTree")
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(df['all_concepts'].values.astype('U'))
    similarity_matrix = cosine_similarity(tfidf, tfidf)
    jsnNW = getNetworkForRadialTree(similarity_matrix, df)
    cats = df[barrier].unique()
    uni_nodes = df[['uri',barrier]]
    
    json_cats = [{"name": t} for t in cats]
    json_nods = [{"category": t, "name": s, "value": 1} for t,s in zip(uni_nodes[barrier], uni_nodes.uri)]
    
    jsnNW["categories"] = json_cats
    jsnNW["nodes"] = json_nods
    
    del jsnNW["directed"]
    del jsnNW["multigraph"]
    del jsnNW["graph"]
    
    jsnNW["type"] = "force"
    
    s1 = json.dumps(jsnNW)
    
    jsonFilew = open("/home/adbuls/visualisation/PropagationNetwork/flaskProject2/app/graphs/static/jsnw.json", "w")
    jsonFilew.write(s1)
    jsonFilew.close()
    
    with open("/home/adbuls/visualisation/PropagationNetwork/flaskProject2/app/graphs/static/jsnw.json") as jsonFile:
        data = json.load(jsonFile)
        data2 = data;
        print(data2)
    return data2
    
    
    
    
    
    