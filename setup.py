from setuptools import setup, find_packages

setup(
    name="chucky-tools",
    version="0.1dev",
    author="Alwin Maier",
    description="Tools for chucky.",
    license="GPLv3",
    url="http://github.com/a0x77n/chucky-tools/",
    install_requires=['joerntools >= 0.1-chucky', 'numpy', 'scipy', 'fastcluster'],
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"chucky_tools": ['data/steps/*.groovy', 'data/steps/normalization/*.groovy',
                                   'data/steps/normalization/handler/*.groovy']},
    entry_points={
        'console_scripts': [
            'chucky-knn = chucky_tools.neighborhood.knn_tool:KNNTool.main',
            'chucky-cluster = chucky_tools.neighborhood.cluster_tool:ClusterTool.main',
            'chucky-normalize = chucky_tools.chucky_normalizer:ChuckyNormalizer.main',
            'chucky-score = chucky_tools.chucky_score_tool:ChuckyScoreTool.main',
            'chucky-demux = chucky_tools.demux_tool:DemuxTool.main',
            'chucky-mux = chucky_tools.mux_tool:MuxTool.main',
            'chucky-taint = chucky_tools.taint_tool:TaintTool.main',
            'chucky-store = chucky_tools.store_tool:StoreTool.main',
            'chucky-traverse = chucky_tools.traversal_tool:TraversalTool.main',
            'chucky-translate = chucky_tools.translate_tool:TranslateTool.main',
        ]
    }
)
