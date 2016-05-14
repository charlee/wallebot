try:
    import opencc
    convert = opencc.convert
except ImportError:
    from hanziconv import HanziConv
    convert = HanziConv.toSimplified
