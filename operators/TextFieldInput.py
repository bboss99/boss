
dict_keys = {
    'A'             :   'a',
    'B'             :   'b',
    'C'             :   'c',
    'D'             :   'd',
    'E'             :   'e',
    'F'             :   'f',
    'G'             :   'g',
    'H'             :   'h',
    'I'             :   'i',
    'J'             :   'j',
    'K'             :   'k',
    'L'             :   'l',
    'M'             :   'm',
    'N'             :   'n',
    'O'             :   'o',
    'P'             :   'p',
    'Q'             :   'q',
    'R'             :   'r',
    'S'             :   's',
    'T'             :   't',
    'U'             :   'u',
    'V'             :   'v',
    'W'             :   'w',
    'X'             :   'x',
    'Y'             :   'y',
    'Z'             :   'z',
    'ZERO'          :   '0',
    'ONE'           :   '1',
    'TWO'           :   '2',
    'THREE'         :   '3',
    'FOUR'          :   '4',
    'FIVE'          :   '5',
    'SIX'           :   '6',
    'SEVEN'         :   '7',
    'EIGHT'         :   '8',
    'NINE'          :   '9',
    'COMMA'         :   ',',
    'PERIOD'        :   '.',
    'LEFT_ARROW'    :   'LEFT_ARROW',
    'DOWN_ARROW'    :   'DOWN_ARROW',
    'RIGHT_ARROW'   :   'RIGHT_ARROW',
    'UP_ARROW'      :   'UP_ARROW',
    'SEMI_COLON'    :   ';',
    'SPACE'         :   ' ',
    'TAB'           :   'TAB',
    'MINUS'         :   '-',
    'EQUAL'         :   '=',
    'SLASH'         :   '/',
    'BACK_SLASH'    :   '\\',
    'HOME'          :   'HOME',
    'END'           :   'END',
    'LEFT_BRACKET'  :   '[',
    'RIGHT_BRACKET' :   ']',
    'BACK_SPACE'    :   'BACK_SPACE',
    'DEL'           :   'DEL',
    'RET'           :   'RET',
    'ACCENT_GRAVE'  :   '`',
    'QUOTE'         :   "'"
}

dict_shift_keys = {
    'A'             :   'A',
    'B'             :   'B',
    'C'             :   'C',
    'D'             :   'D',
    'E'             :   'E',
    'F'             :   'F',
    'G'             :   'G',
    'H'             :   'H',
    'I'             :   'I',
    'J'             :   'J',
    'K'             :   'K',
    'L'             :   'L',
    'M'             :   'M',
    'N'             :   'N',
    'O'             :   'O',
    'P'             :   'P',
    'Q'             :   'Q',
    'R'             :   'R',
    'S'             :   'S',
    'T'             :   'T',
    'U'             :   'U',
    'V'             :   'V',
    'W'             :   'W',
    'X'             :   'X',
    'Y'             :   'Y',
    'Z'             :   'Z',

    'ZERO'          :   ')',
    'ONE'           :   '!',
    'TWO'           :   '@',
    'THREE'         :   '#',
    'FOUR'          :   '$',
    'FIVE'          :   '%',
    'SIX'           :   '^',
    'SEVEN'         :   '&',
    'EIGHT'         :   '*',
    'NINE'          :   '(',
    'COMMA'         :   '<',
    'PERIOD'        :   '>',
    'SEMI_COLON'    :   ':',
    'MINUS'         :   '_',
    'EQUAL'         :   '+',
    'SLASH'         :   '?',
    'BACK_SLASH'    :   '|',
    'LEFT_BRACKET'  :   '{',
    'RIGHT_BRACKET' :   '}',
    'ACCENT_GRAVE'  :   '~',
    'QUOTE'         :   '"'
}

dict_keys_mod = {
    'LEFT_SHIFT'    :   'LEFT_SHIFT',
    'RIGHT_SHIFT'   :   'RIGHT_SHIFT',
    'LEFT_ALT'      :   'LEFT_ALT',
    'RIGHT_ALT'     :   'RIGHT_ALT',
    'LEFT_CTRL'     :   'LEFT_CTRL',
    'RIGHT_CTRL'    :   'RIGHT_CTRL',
}

shiftKeys   = ('LEFT_SHIFT','RIGHT_SHIFT')
ctrlKeys    = ('LEFT_CTRL','RIGHT_CTRL')
altKeys    = ('LEFT_ALT','RIGHT_ALT')

def takeTextFieldInput(uip,event):
    if(event.value == 'PRESS'):
        if event.type in shiftKeys:
            uip.shift_pressed = True

        if event.type in ctrlKeys:
            uip.ctrl_pressed = True

        if event.type in altKeys:
            uip.alt_pressed = True

        if event.type in dict_keys:
            if event.type in dict_shift_keys:
                if uip.shift_pressed:
                    uip.keyPress(dict_shift_keys[event.type])
                else:
                    uip.keyPress(dict_keys[event.type])
            else:
                uip.keyPress(dict_keys[event.type])

    elif(event.value == 'RELEASE'):
        if event.type == 'ESC':
            uip.textFieldResetFunc()

        if event.type in shiftKeys:
            uip.shift_pressed = False

        if event.type in ctrlKeys:
            uip.ctrl_pressed = False

        if event.type in altKeys:
            uip.alt_pressed = False


