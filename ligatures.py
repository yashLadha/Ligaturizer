## This is the master list of ligatures that ligaturize.py will attempt to copy
## from Fira Code to your output font. Ligatures that aren't present in the
## version of Fira Code you're using will be skipped.
## To disable ligatures, simply comment them out in this file.
ligatures = [
    {
        ## These are all the punctuation characters used in Fira Code ligatures.
        ## Use the `--copy-character-glyphs` option to copy these into the output
        ## font along with the ligatures themselves.
        'chars': [
            ## These characters generally look good in most fonts and are
            ## enabled by default if you use `--copy-character-glyphs`.
            'ampersand', 'asciicircum', 'asciitilde', 'asterisk',
            'backslash', 'bar',
            'colon', 'equal', 'exclam', 'greater', 'hyphen',
            'less', 'numbersign', 'percent', 'period', 'plus',
            'question', 'semicolon', 'slash', 'underscore',

            ## These characters are also used by the ligatures, but are likely
            ## to look more out of place when spliced into another font.
            # 'at', 'braceleft', 'braceright', 'bracketleft', 'bracketright',
            # 'dollar', 'parenleft', 'parenright', 'underscore', 'w'
        ],
        'firacode_ligature_name': None,
    },
    ## These are traditional (i.e. present in most variable-width fonts)
    ## aesthetic ligatures. They are commented out here so that they don't
    ## overwrite similar ligatures present in the destination font.
    # {   # Fl
    #     'chars': ['F', 'l'],
    #     'firacode_ligature_name': 'F_l.liga',
    # },
    # {   # Tl
    #     'chars': ['T', 'l'],
    #     'firacode_ligature_name': 'T_l.liga',
    # },
    # {   # fi
    #     'chars': ['f', 'i'],
    #     'firacode_ligature_name': 'f_i.liga',
    # },
    # {   # fj
    #     'chars': ['f', 'j'],
    #     'firacode_ligature_name': 'f_j.liga',
    # },
    # {   # fl
    #     'chars': ['f', 'l'],
    #     'firacode_ligature_name': 'f_l.liga',
    # },
    # {   # ft
    #     'chars': ['f', 't'],
    #     'firacode_ligature_name': 'f_t.liga',
    # },
    ## Programming ligatures begin here.
    {   # &&
        'chars': ['ampersand', 'ampersand'],
        'firacode_ligature_name': 'ampersand_ampersand.liga',
    },
    {   # ^=
        'chars': ['asciicircum', 'equal'],
        'firacode_ligature_name': 'asciicircum_equal.liga',
    },
    {   # ~~
        'chars': ['asciitilde', 'asciitilde'],
        'firacode_ligature_name': 'asciitilde_asciitilde.liga',
    },
    {   # ~~>
        'chars': ['asciitilde', 'asciitilde', 'greater'],
        'firacode_ligature_name': 'asciitilde_asciitilde_greater.liga',
    },
    {   # ~@
        'chars': ['asciitilde', 'at'],
        'firacode_ligature_name': 'asciitilde_at.liga',
    },
    ## Removed in Fira Code v6:
    # {   # ~=
    #     'chars': ['asciitilde', 'equal'],
    #     'firacode_ligature_name': 'asciitilde_equal.liga',
    # },
    {   # ~>
        'chars': ['asciitilde', 'greater'],
        'firacode_ligature_name': 'asciitilde_greater.liga',
    },
    {   # ~-
        'chars': ['asciitilde', 'hyphen'],
        'firacode_ligature_name': 'asciitilde_hyphen.liga',
    },
    {   # **
        'chars': ['asterisk', 'asterisk'],
        'firacode_ligature_name': 'asterisk_asterisk.liga',
    },
    {   # ***
        'chars': ['asterisk', 'asterisk', 'asterisk'],
        'firacode_ligature_name': 'asterisk_asterisk_asterisk.liga',
    },
    {   # *>
        'chars': ['asterisk', 'greater'],
        'firacode_ligature_name': 'asterisk_greater.liga',
    },
    {   # */
        'chars': ['asterisk', 'slash'],
        'firacode_ligature_name': 'asterisk_slash.liga',
    },
    {   # \/
        'chars': ['backslash', 'slash'],
        'firacode_ligature_name': 'backslash_slash.liga',
    },
    {   # ||
        'chars': ['bar', 'bar'],
        'firacode_ligature_name': 'bar_bar.liga',
    },
    {   # ||| (new in Fira Code v6)
        'chars': ['bar', 'bar', 'bar'],
        'firacode_ligature_name': 'bar_bar_bar.liga',
    },
    {   # |||>
        'chars': ['bar', 'bar', 'bar', 'greater'],
        'firacode_ligature_name': 'bar_bar_bar_greater.liga',
    },
    {   # ||=
        'chars': ['bar', 'bar', 'equal'],
        'firacode_ligature_name': 'bar_bar_equal.liga',
        'seq_components': ['bar_bar_equal_start.seq', 'equal_middle.seq', 'equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # ||>
        'chars': ['bar', 'bar', 'greater'],
        'firacode_ligature_name': 'bar_bar_greater.liga',
    },
    {   # ||-
        'chars': ['bar', 'bar', 'hyphen'],
        'firacode_ligature_name': 'bar_bar_hyphen.liga',
        'seq_components': ['bar_bar_hyphen_start.seq', 'hyphen_middle.seq', 'hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # |}
        'chars': ['bar', 'braceright'],
        'firacode_ligature_name': 'bar_braceright.liga',
    },
    {   # |]
        'chars': ['bar', 'bracketright'],
        'firacode_ligature_name': 'bar_bracketright.liga',
    },
    {   # |=
        'chars': ['bar', 'equal'],
        'firacode_ligature_name': 'bar_equal.liga',
        'seq_components': ['bar_equal_start.seq', 'equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # |=>
        'chars': ['bar', 'equal', 'greater'],
        'firacode_ligature_name': 'bar_equal_greater.liga',
        'seq_components': ['bar_equal_start.seq', 'greater_equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # |>
        'chars': ['bar', 'greater'],
        'firacode_ligature_name': 'bar_greater.liga',
    },
    {   # |-
        'chars': ['bar', 'hyphen'],
        'firacode_ligature_name': 'bar_hyphen.liga',
        'seq_components': ['bar_hyphen_start.seq', 'hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # |->
        'chars': ['bar', 'hyphen', 'greater'],
        'firacode_ligature_name': 'bar_hyphen_greater.liga',
        'seq_components': ['bar_hyphen_start.seq', 'greater_hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # {|
        'chars': ['braceleft', 'bar'],
        'firacode_ligature_name': 'braceleft_bar.liga',
    },
    {   # [|
        'chars': ['bracketleft', 'bar'],
        'firacode_ligature_name': 'bracketleft_bar.liga',
    },
    {   # ]#
        'chars': ['bracketright', 'numbersign'],
        'firacode_ligature_name': 'bracketright_numbersign.liga',
    },
    {   # ::
        'chars': ['colon', 'colon'],
        'firacode_ligature_name': 'colon_colon.liga',
    },
    {   # :::
        'chars': ['colon', 'colon', 'colon'],
        'firacode_ligature_name': 'colon_colon_colon.liga',
    },
    {   # ::=
        'chars': ['colon', 'colon', 'equal'],
        'firacode_ligature_name': 'colon_colon_equal.liga',
    },
    {   # :=
        'chars': ['colon', 'equal'],
        'firacode_ligature_name': 'colon_equal.liga',
    },
    ## Removed in Fira Code v6:
    # {   # :>
    #     'chars': ['colon', 'greater'],
    #     'firacode_ligature_name': 'colon_greater.liga',
    # },
    ## Removed in Fira Code v6:
    # {   # :<
    #     'chars': ['colon', 'less'],
    #     'firacode_ligature_name': 'colon_less.liga',
    # },
    {   # $>
        'chars': ['dollar', 'greater'],
        'firacode_ligature_name': 'dollar_greater.liga',
    },
    {   # =:=
        'chars': ['equal', 'colon', 'equal'],
        'firacode_ligature_name': 'equal_colon_equal.liga',
        'seq_components': ['equal_start.seq', 'colon_equal_middle.seq', 'equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # ==
        'chars': ['equal', 'equal'],
        'firacode_ligature_name': 'equal_equal.liga',
    },
    {   # ===
        'chars': ['equal', 'equal', 'equal'],
        'firacode_ligature_name': 'equal_equal_equal.liga',
    },
    {   # ==>
        'chars': ['equal', 'equal', 'greater'],
        'firacode_ligature_name': 'equal_equal_greater.liga',
        'seq_components': ['equal_start.seq', 'equal_middle.seq', 'greater_equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # =!=
        'chars': ['equal', 'exclam', 'equal'],
        'firacode_ligature_name': 'equal_exclam_equal.liga',
        'seq_components': ['equal_start.seq', 'exclam_equal_middle.seq', 'equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # =>
        'chars': ['equal', 'greater'],
        'firacode_ligature_name': 'equal_greater.liga',
        'seq_components': ['equal_start.seq', 'greater_equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # =>>
        'chars': ['equal', 'greater', 'greater'],
        'firacode_ligature_name': 'equal_greater_greater.liga',
        'seq_components': ['equal_start.seq', 'greater_greater_equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # =<<
        'chars': ['equal', 'less', 'less'],
        'firacode_ligature_name': 'equal_less_less.liga',
        'seq_components': ['equal_start.seq', 'less_less_equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # =/=
        'chars': ['equal', 'slash', 'equal'],
        'firacode_ligature_name': 'equal_slash_equal.liga',
        'seq_components': ['equal_start.seq', 'slash_equal_middle.seq', 'equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # !=
        'chars': ['exclam', 'equal'],
        'firacode_ligature_name': 'exclam_equal.liga',
    },
    {   # !==
        'chars': ['exclam', 'equal', 'equal'],
        'firacode_ligature_name': 'exclam_equal_equal.liga',
    },
    {   # !!
        'chars': ['exclam', 'exclam'],
        'firacode_ligature_name': 'exclam_exclam.liga',
    },
    {   # !!.
        'chars': ['exclam', 'exclam', 'period'],
        'firacode_ligature_name': 'exclam_exclam_period.liga',
    },
    ## Removed in Fira Code v6:
    # {   # >:
    #     'chars': ['greater', 'colon'],
    #     'firacode_ligature_name': 'greater_colon.liga',
    # },
    {   # >=
        'chars': ['greater', 'equal'],
        'firacode_ligature_name': 'greater_equal.liga',
    },
    {   # >=>
        'chars': ['greater', 'equal', 'greater'],
        'firacode_ligature_name': 'greater_equal_greater.liga',
        'seq_components': ['greater_equal_start.seq', 'greater_equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # >>
        'chars': ['greater', 'greater'],
        'firacode_ligature_name': 'greater_greater.liga',
    },
    {   # >>=
        'chars': ['greater', 'greater', 'equal'],
        'firacode_ligature_name': 'greater_greater_equal.liga',
        'seq_components': ['greater_greater_equal_start.seq', 'equal_middle.seq', 'equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # >>>
        'chars': ['greater', 'greater', 'greater'],
        'firacode_ligature_name': 'greater_greater_greater.liga',
    },
    {   # >>-
        'chars': ['greater', 'greater', 'hyphen'],
        'firacode_ligature_name': 'greater_greater_hyphen.liga',
        'seq_components': ['greater_greater_hyphen_start.seq', 'hyphen_middle.seq', 'hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # >-
        'chars': ['greater', 'hyphen'],
        'firacode_ligature_name': 'greater_hyphen.liga',
        'seq_components': ['greater_hyphen_start.seq', 'hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # >->
        'chars': ['greater', 'hyphen', 'greater'],
        'firacode_ligature_name': 'greater_hyphen_greater.liga',
        'seq_components': ['greater_hyphen_start.seq', 'greater_hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # -~
        'chars': ['hyphen', 'asciitilde'],
        'firacode_ligature_name': 'hyphen_asciitilde.liga',
    },
    {   # -|
        'chars': ['hyphen', 'bar'],
        'firacode_ligature_name': 'hyphen_bar.liga',
        'seq_components': ['hyphen_start.seq', 'bar_hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # ->
        'chars': ['hyphen', 'greater'],
        'firacode_ligature_name': 'hyphen_greater.liga',
        'seq_components': ['hyphen_start.seq', 'greater_hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # ->>
        'chars': ['hyphen', 'greater', 'greater'],
        'firacode_ligature_name': 'hyphen_greater_greater.liga',
        'seq_components': ['hyphen_start.seq', 'greater_greater_hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # --
        'chars': ['hyphen', 'hyphen'],
        'firacode_ligature_name': 'hyphen_hyphen.liga',
    },
    {   # -->
        'chars': ['hyphen', 'hyphen', 'greater'],
        'firacode_ligature_name': 'hyphen_hyphen_greater.liga',
        'seq_components': ['hyphen_start.seq', 'hyphen_middle.seq', 'greater_hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # ---
        'chars': ['hyphen', 'hyphen', 'hyphen'],
        'firacode_ligature_name': 'hyphen_hyphen_hyphen.liga',
        'seq_components': ['hyphen_start.seq', 'hyphen_middle.seq', 'hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # -<
        'chars': ['hyphen', 'less'],
        'firacode_ligature_name': 'hyphen_less.liga',
        'seq_components': ['hyphen_start.seq', 'less_hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # -<<
        'chars': ['hyphen', 'less', 'less'],
        'firacode_ligature_name': 'hyphen_less_less.liga',
        'seq_components': ['hyphen_start.seq', 'less_less_hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # <~
        'chars': ['less', 'asciitilde'],
        'firacode_ligature_name': 'less_asciitilde.liga',
    },
    {   # <~~
        'chars': ['less', 'asciitilde', 'asciitilde'],
        'firacode_ligature_name': 'less_asciitilde_asciitilde.liga',
    },
    {   # <~>
        'chars': ['less', 'asciitilde', 'greater'],
        'firacode_ligature_name': 'less_asciitilde_greater.liga',
    },
    {   # <*
        'chars': ['less', 'asterisk'],
        'firacode_ligature_name': 'less_asterisk.liga',
    },
    {   # <*>
        'chars': ['less', 'asterisk', 'greater'],
        'firacode_ligature_name': 'less_asterisk_greater.liga',
    },
    {   # <|
        'chars': ['less', 'bar'],
        'firacode_ligature_name': 'less_bar.liga',
    },
    {   # <||
        'chars': ['less', 'bar', 'bar'],
        'firacode_ligature_name': 'less_bar_bar.liga',
    },
    {   # <|||
        'chars': ['less', 'bar', 'bar', 'bar'],
        'firacode_ligature_name': 'less_bar_bar_bar.liga',
    },
    {   # <|>
        'chars': ['less', 'bar', 'greater'],
        'firacode_ligature_name': 'less_bar_greater.liga',
    },
    {   # <:
        'chars': ['less', 'colon'],
        'firacode_ligature_name': 'less_colon.liga',
    },
    {   # <$
        'chars': ['less', 'dollar'],
        'firacode_ligature_name': 'less_dollar.liga',
    },
    {   # <$>
        'chars': ['less', 'dollar', 'greater'],
        'firacode_ligature_name': 'less_dollar_greater.liga',
    },
    {   # <=
        'chars': ['less', 'equal'],
        'firacode_ligature_name': 'less_equal.liga',
    },
    {   # <=|
        'chars': ['less', 'equal', 'bar'],
        'firacode_ligature_name': 'less_equal_bar.liga',
        'seq_components': ['less_equal_start.seq', 'bar_equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # <==
        'chars': ['less', 'equal', 'equal'],
        'firacode_ligature_name': 'less_equal_equal.liga',
        'seq_components': ['less_equal_start.seq', 'equal_middle.seq', 'equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # <==>
        'chars': ['less', 'equal', 'equal', 'greater'],
        'firacode_ligature_name': 'less_equal_equal_greater.liga',
        'seq_components': ['less_equal_start.seq', 'equal_middle.seq', 'greater_equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # <=>
        'chars': ['less', 'equal', 'greater'],
        'firacode_ligature_name': 'less_equal_greater.liga',
        'seq_components': ['less_equal_start.seq', 'greater_equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # <=<
        'chars': ['less', 'equal', 'less'],
        'firacode_ligature_name': 'less_equal_less.liga',
        'seq_components': ['less_equal_start.seq', 'less_equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # <!--
        'chars': ['less', 'exclam', 'hyphen', 'hyphen'],
        'firacode_ligature_name': 'less_exclam_hyphen_hyphen.liga',
    },
    {   # <>
        'chars': ['less', 'greater'],
        'firacode_ligature_name': 'less_greater.liga',
    },
    {   # <-
        'chars': ['less', 'hyphen'],
        'firacode_ligature_name': 'less_hyphen.liga',
        'seq_components': ['less_hyphen_start.seq', 'hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # <-|
        'chars': ['less', 'hyphen', 'bar'],
        'firacode_ligature_name': 'less_hyphen_bar.liga',
        'seq_components': ['less_hyphen_start.seq', 'bar_hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # <->
        'chars': ['less', 'hyphen', 'greater'],
        'firacode_ligature_name': 'less_hyphen_greater.liga',
        'seq_components': ['less_hyphen_start.seq', 'greater_hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # <--
        'chars': ['less', 'hyphen', 'hyphen'],
        'firacode_ligature_name': 'less_hyphen_hyphen.liga',
        'seq_components': ['less_hyphen_start.seq', 'hyphen_middle.seq', 'hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # <-<
        'chars': ['less', 'hyphen', 'less'],
        'firacode_ligature_name': 'less_hyphen_less.liga',
        'seq_components': ['less_hyphen_start.seq', 'less_hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # <<
        'chars': ['less', 'less'],
        'firacode_ligature_name': 'less_less.liga',
    },
    {   # <<=
        'chars': ['less', 'less', 'equal'],
        'firacode_ligature_name': 'less_less_equal.liga',
        'seq_components': ['less_less_equal_start.seq', 'equal_middle.seq', 'equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # <<-
        'chars': ['less', 'less', 'hyphen'],
        'firacode_ligature_name': 'less_less_hyphen.liga',
        'seq_components': ['less_less_hyphen_start.seq', 'hyphen_middle.seq', 'hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # <<->>
        'chars': ['less', 'less', 'hyphen', 'greater', 'greater'],
        'firacode_ligature_name': 'less_less_hyphen_greater_greater.liga',
        'seq_components': ['less_less_hyphen_start.seq', 'hyphen_middle.seq', 'greater_greater_hyphen_end.seq'],
        'handled_by_seq': True,
    },
    {   # <<<
        'chars': ['less', 'less', 'less'],
        'firacode_ligature_name': 'less_less_less.liga',
    },
    {   # <+
        'chars': ['less', 'plus'],
        'firacode_ligature_name': 'less_plus.liga',
    },
    {   # <+>
        'chars': ['less', 'plus', 'greater'],
        'firacode_ligature_name': 'less_plus_greater.liga',
    },
    # {   # </
    #     'chars': ['less', 'slash'],
    #     'firacode_ligature_name': 'less_slash.liga',
    # },
    # {   # </>
    #     'chars': ['less', 'slash', 'greater'],
    #     'firacode_ligature_name': 'less_slash_greater.liga',
    # },
    {   # #{
        'chars': ['numbersign', 'braceleft'],
        'firacode_ligature_name': 'numbersign_braceleft.liga',
    },
    {   # #[
        'chars': ['numbersign', 'bracketleft'],
        'firacode_ligature_name': 'numbersign_bracketleft.liga',
    },
    {   # #:
        'chars': ['numbersign', 'colon'],
        'firacode_ligature_name': 'numbersign_colon.liga',
    },
    {   # #=
        'chars': ['numbersign', 'equal'],
        'firacode_ligature_name': 'numbersign_equal.liga',
    },
    {   # #!
        'chars': ['numbersign', 'exclam'],
        'firacode_ligature_name': 'numbersign_exclam.liga',
    },
    {   # ##
        'chars': ['numbersign', 'numbersign'],
        'firacode_ligature_name': 'numbersign_numbersign.liga',
        'seq_components': ['numbersign_start.seq', 'numbersign_end.seq'],
    },
    {   # ###
        'chars': ['numbersign', 'numbersign', 'numbersign'],
        'firacode_ligature_name': 'numbersign_numbersign_numbersign.liga',
        'seq_components': ['numbersign_start.seq', 'numbersign_middle.seq', 'numbersign_end.seq'],
    },
    {   # ####
        'chars': ['numbersign', 'numbersign', 'numbersign', 'numbersign'],
        'firacode_ligature_name': 'numbersign_numbersign_numbersign_numbersign.liga',
        'seq_components': ['numbersign_start.seq', 'numbersign_middle.seq', 'numbersign_middle.seq', 'numbersign_end.seq'],
    },
    {   # #(
        'chars': ['numbersign', 'parenleft'],
        'firacode_ligature_name': 'numbersign_parenleft.liga',
    },
    {   # #?
        'chars': ['numbersign', 'question'],
        'firacode_ligature_name': 'numbersign_question.liga',
    },
    {   # #_
        'chars': ['numbersign', 'underscore'],
        'firacode_ligature_name': 'numbersign_underscore.liga',
    },
    {   # #_(
        'chars': ['numbersign', 'underscore', 'parenleft'],
        'firacode_ligature_name': 'numbersign_underscore_parenleft.liga',
    },
    {   # %%
        'chars': ['percent', 'percent'],
        'firacode_ligature_name': 'percent_percent.liga',
    },
    {   # .=
        'chars': ['period', 'equal'],
        'firacode_ligature_name': 'period_equal.cv32',
    },
    {   # .-
        'chars': ['period', 'hyphen'],
        'firacode_ligature_name': 'period_hyphen.cv25',
    },
    {   # ..
        'chars': ['period', 'period'],
        'firacode_ligature_name': 'period_period.liga',
    },
    {   # ..=
        'chars': ['period', 'period', 'equal'],
        'firacode_ligature_name': 'period_period_equal.liga',
    },
    {   # ..<
        'chars': ['period', 'period', 'less'],
        'firacode_ligature_name': 'period_period_less.liga',
    },
    {   # ...
        'chars': ['period', 'period', 'period'],
        'firacode_ligature_name': 'period_period_period.liga',
    },
    {   # .?
        'chars': ['period', 'question'],
        'firacode_ligature_name': 'period_question.liga',
    },
    {   # +>
        'chars': ['plus', 'greater'],
        'firacode_ligature_name': 'plus_greater.liga',
    },
    {   # ++
        'chars': ['plus', 'plus'],
        'firacode_ligature_name': 'plus_plus.liga',
    },
    {   # +++
        'chars': ['plus', 'plus', 'plus'],
        'firacode_ligature_name': 'plus_plus_plus.liga',
    },
    ## Removed in Fira Code v6:
    # {   # ?:
    #     'chars': ['question', 'colon'],
    #     'firacode_ligature_name': 'question_colon.liga',
    # },
    {   # ?=
        'chars': ['question', 'equal'],
        'firacode_ligature_name': 'question_equal.liga',
    },
    {   # ?.
        'chars': ['question', 'period'],
        'firacode_ligature_name': 'question_period.liga',
    },
    {   # ??
        'chars': ['question', 'question'],
        'firacode_ligature_name': 'question_question.liga',
    },
    {   # ;;
        'chars': ['semicolon', 'semicolon'],
        'firacode_ligature_name': 'semicolon_semicolon.liga',
    },
    {   # /*
        'chars': ['slash', 'asterisk'],
        'firacode_ligature_name': 'slash_asterisk.liga',
    },
    {   # /\
        'chars': ['slash', 'backslash'],
        'firacode_ligature_name': 'slash_backslash.liga',
    },
    {   # /=
        'chars': ['slash', 'equal'],
        'firacode_ligature_name': 'slash_equal.liga',
        'seq_components': ['slash_equal_start.seq', 'equal_end.seq'],
        'handled_by_seq': True,
    },
    {   # /==
        'chars': ['slash', 'equal', 'equal'],
        'firacode_ligature_name': 'slash_equal_equal.liga',
        'seq_components': ['slash_equal_start.seq', 'equal_middle.seq', 'equal_end.seq'],
        'handled_by_seq': True,
    },
    # {   # />
    #     'chars': ['slash', 'greater'],
    #     'firacode_ligature_name': 'slash_greater.liga',
    # },
    {   # //
        'chars': ['slash', 'slash'],
        'firacode_ligature_name': 'slash_slash.liga',
    },
    {   # ///
        'chars': ['slash', 'slash', 'slash'],
        'firacode_ligature_name': 'slash_slash_slash.liga',
    },
    {   # _|_
        'chars': ['underscore', 'bar', 'underscore'],
        'firacode_ligature_name': 'underscore_bar_underscore.liga',
        'seq_components': ['underscore_start.seq', 'bar_underscore_middle.seq', 'underscore_end.seq'],
    },
    {   # __
        'chars': ['underscore', 'underscore'],
        'firacode_ligature_name': 'underscore_underscore.liga',
        'seq_components': ['underscore_start.seq', 'underscore_end.seq'],
    },
    {   # www
        'chars': ['w', 'w', 'w'],
        'firacode_ligature_name': 'w_w_w.liga',
    },
]

seq_families = [
    {
        'name': 'equal_arrows',
        'base_char': 'equal',
        'spacer': 'equal.spacer',
        'start_seq': 'equal_start.seq',
        'middle_seq': 'equal_middle.seq',
        'end_seq': 'equal_end.seq',
        'terminators': ['greater', 'less', 'bar', 'slash'],
        'compound_terminators': ['colon', 'exclam'],
        # Terminators whose 2-char ligature (e.g. <=, >=) uses a .liga glyph.
        # The seq start rules will require a longer lookahead for these so
        # the fixed .liga ligature handles the 2-char case instead.
        'liga_terminators': ['less', 'greater'],
        'ignore_rules': {
            'equal': [
                # Protect == and === from Phase A spacer conversion.
                # Phase B handles ==== and longer directly without Phase A.
                {'lookahead': ['equal']},
                # Protect === (triple equals) and longer fixed patterns
                {'backtrack': ['equal'], 'lookahead': ['equal', 'equal']},
                {'lookahead': ['equal', 'equal', 'equal']},
                # Protect (?= (?== (?<= patterns
                {'backtrack': ['question', 'parenleft'], 'lookahead': ['equal', 'equal']},
                {'backtrack': ['less', 'question', 'parenleft'], 'lookahead': ['equal', 'equal']},
                {'backtrack': ['question', 'less'], 'lookahead': ['equal', 'equal']},
                # Protect [== ==] patterns
                {'backtrack': ['bracketleft'], 'lookahead': ['equal', 'equal']},
                {'lookahead': ['equal', 'equal', 'bracketright']},
                # Protect !== :== patterns
                {'backtrack': [['colon', 'exclam'], 'equal'], 'lookahead': ['equal', 'equal']},
                # Protect |== /== >== <== patterns (terminator prefix)
                {'backtrack': [['slash', 'bar', 'greater', 'less']], 'lookahead': ['equal', 'equal']},
                {'lookahead': ['equal', 'equal', ['slash', 'bar', 'greater', 'less']]},
                # Protect =:= =!= patterns
                {'lookahead': ['equal', 'equal', ['colon', 'exclam'], 'equal']},
            ],
        },
        # Seq assignment helper lookup mappings (from Fira Code TTX analysis)
        'middle_lookup': {
            'colon': 'colon_equal_middle.seq',
            'exclam': 'exclam_equal_middle.seq',
            'slash': 'slash_slash_equal_middle.seq',
            'bar': 'bar_bar_equal_middle.seq',
            'equal': 'equal_middle.seq',
            'greater': 'greater_greater_equal_middle.seq',
            'less': 'less_less_equal_middle.seq',
        },
        'end_spacer_lookup': {
            'slash': 'slash.spacer',
            'bar': 'bar.spacer',
            'equal': 'equal_end.seq',
            'greater': 'greater.spacer',
            'less': 'less.spacer',
        },
        'single_term_middle_lookup': {
            'slash': 'slash_equal_middle.seq',
            'bar': 'bar_equal_middle.seq',
            'equal': 'equal_start.seq',
            'greater': 'greater_equal_middle.seq',
            'less': 'less_equal_middle.seq',
        },
        'double_term_end_lookup': {
            'slash': 'slash_slash_equal_end.seq',
            'bar': 'bar_bar_equal_end.seq',
            'equal': 'equal_start.seq',
            'greater': 'greater_greater_equal_end.seq',
            'less': 'less_less_equal_end.seq',
        },
        'start_spacer_lookup': {
            'slash': 'slash.spacer',
            'bar': 'bar.spacer',
            'equal': 'equal_start.seq',
            'greater': 'greater.spacer',
            'less': 'less.spacer',
        },
        'single_term_end_lookup': {
            'slash': 'slash_equal_end.seq',
            'bar': 'bar_equal_end.seq',
            'greater': 'greater_equal_end.seq',
            'less': 'less_equal_end.seq',
        },
        'double_term_start_lookup': {
            'slash': 'slash_slash_equal_start.seq',
            'bar': 'bar_bar_equal_start.seq',
            'greater': 'greater_greater_equal_start.seq',
            'less': 'less_less_equal_start.seq',
        },
        'double_term_spacer_lookup': {
            'slash': 'slash.spacer',
            'bar': 'bar.spacer',
            'greater': 'greater.spacer',
            'less': 'less.spacer',
        },
        'single_term_start_lookup': {
            'slash': 'slash_equal_start.seq',
            'bar': 'bar_equal_start.seq',
            'greater': 'greater_equal_start.seq',
            'less': 'less_equal_start.seq',
        },
    },
    {
        'name': 'hyphen_arrows',
        'base_char': 'hyphen',
        'spacer': 'hyphen.spacer',
        'start_seq': 'hyphen_start.seq',
        'middle_seq': 'hyphen_middle.seq',
        'end_seq': 'hyphen_end.seq',
        'terminators': ['greater', 'less', 'bar'],
        'compound_terminators': [],
        'seq_handles_triple': True,
        # No ignore rules needed: Phase A action rules require 2+ hyphens
        # in lookahead, so -- (2-char) is naturally unaffected. Terminator
        # patterns like |-- and <-- are handled by Phase B start rules.
        'ignore_rules': {},
        'middle_lookup': {
            'hyphen': 'hyphen_middle.seq',
            'bar': 'bar_bar_hyphen_middle.seq',
            'greater': 'greater_greater_hyphen_middle.seq',
            'less': 'less_less_hyphen_middle.seq',
        },
        'end_spacer_lookup': {
            'hyphen': 'hyphen_end.seq',
            'bar': 'bar.spacer',
            'greater': 'greater.spacer',
            'less': 'less.spacer',
        },
        'single_term_middle_lookup': {
            'hyphen': 'hyphen_start.seq',
            'bar': 'bar_hyphen_middle.seq',
            'greater': 'greater_hyphen_middle.seq',
            'less': 'less_hyphen_middle.seq',
        },
        'double_term_end_lookup': {
            'bar': 'bar_bar_hyphen_end.seq',
            'greater': 'greater_greater_hyphen_end.seq',
            'less': 'less_less_hyphen_end.seq',
        },
        'start_spacer_lookup': {
            'bar': 'bar.spacer',
            'greater': 'greater.spacer',
            'less': 'less.spacer',
        },
        'single_term_end_lookup': {
            'bar': 'bar_hyphen_end.seq',
            'greater': 'greater_hyphen_end.seq',
            'less': 'less_hyphen_end.seq',
        },
        'double_term_start_lookup': {
            'bar': 'bar_bar_hyphen_start.seq',
            'greater': 'greater_greater_hyphen_start.seq',
            'less': 'less_less_hyphen_start.seq',
        },
        'double_term_spacer_lookup': {
            'bar': 'bar.spacer',
            'greater': 'greater.spacer',
            'less': 'less.spacer',
        },
        'single_term_start_lookup': {
            'bar': 'bar_hyphen_start.seq',
            'greater': 'greater_hyphen_start.seq',
            'less': 'less_hyphen_start.seq',
        },
    },
]