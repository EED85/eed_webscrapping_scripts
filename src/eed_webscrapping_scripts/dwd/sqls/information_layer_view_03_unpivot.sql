UNPIVOT dwd.information_layer.Pollenflug_Gefahrenindex_02
ON Roggen, Birke, Hasel, Ambrosia, Beifuss, Graeser, Erle, Esche
INTO
    NAME pollenart
    VALUE Pollenflug_Gefahrenindex
