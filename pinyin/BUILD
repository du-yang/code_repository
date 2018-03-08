load("//tensorflow:tensorflow.bzl", "tf_cc_binary")

tf_cc_binary(
    name="my_loader",
    srcs=["load_graph_with_c++.cc"],
    deps=[
        "//tensorflow/core:tensorflow",
    ]
)

tf_cc_binary(
    name="dssm",
    srcs=["dssm.cc"],
    deps=[
        "//tensorflow/core:tensorflow",
    ]
)

tf_cc_binary(
    name="pinyin",
    srcs=["main.cc",
          "pinyin.cc",
          "pinyin.h",
          "tf_model.cc",
          "tf_model.h"
         ],
    deps=[
         "//tensorflow/core:tensorflow",
    ]
)

tf_cc_binary(
    name="tftest",
    srcs=["test_main.cc","tf_model.cc","tf_model.h"],
    deps=[
        "//tensorflow/core:tensorflow",
    ]
)
