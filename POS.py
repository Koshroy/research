import ply.lex
import ply.yacc

class POSLexer(object):

    tokens = (
        'LPAREN', 'RPAREN',
        'POS', 'TEXT', 'DOT'
        )

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_POS = r'CC|CD|DT|EX|FW|IN|JJR|JJS|JJ|LS|MD|NNS|NNP|NNPS|NP|NN|PDT|POS|PRP\$|PRP|RB|RBR|RBS|RP|SYM|TO|UH|VBD|VBG|VBN|VBP|VBZ|VB|VP|WDT|WP\$|WP|WRB|ROOT|S'
    t_DOT = r'\.'
    t_TEXT = r'[a-zA-Z]+'
#t_WSPC = r'\s+'

    def t_wspc(self, t):
        r'\s+'

    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = ply.lex.lex(object=self, **kwargs)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        g = self.lexer.token()
        return g

    def tokenize(self, data):
        self.lexer.input(data)

class POSParser(object):
    def __init__(self):
        self.lexer = POSLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = ply.yacc.yacc(module=self)

    def p_sentence_parse(self, p):
        """
        sentence : LPAREN POS sentence sentence sentence RPAREN
        sentence : LPAREN POS sentence sentence RPAREN
        sentence : LPAREN POS sentence RPAREN
        sentence : base_sentence
        """
        if len(p) == 7:
            p[0] = {"pos":p[2], "type" : "pos", "args" : [p[3], p[4], p[5]]}
        elif len(p) == 6:
            p[0] = {"pos":p[2], "type" : "pos", "args" : [p[3], p[4]]}
        elif len(p) == 5:
            p[0] = {"pos":p[2], "type" : "pos", "args" : [p[3]]}
        else:
            p[0] = p[1]

    def p_base_sentence_parse(self, p):
        """
        base_sentence : pos_base
        base_sentence : dot_base
        """
        p[0] = p[1]

    def p_pos_base_parse(self, p):
        """
        pos_base : LPAREN POS TEXT RPAREN
        """
        p[0] = {"pos" : p[2], "type" : "text", "args" : [p[3]]}

    def p_pos_dot_parse(self, p):
        """
        dot_base : LPAREN DOT DOT RPAREN
        """
        p[0] = {"pos" : p[2], "type" : "dot", "args" : [p[3]]}

    def p_error(self, p):
        print "Syntax error at '%s'. Next token: '%s'." % (p.value, ply.yacc.token())


    def parse(self, text):
        print text
        return self.parser.parse(text, lexer=self.lexer)
