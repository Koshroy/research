import ply.lex
import ply.yacc

class POSLexer(object):

    tokens = (
        'LPAREN', 'RPAREN',
        'TEXT', 'PUNCT',
        'CLAUSE_POS', 'PHRASE_POS', 'WORD_POS'
        )

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_CLAUSE_POS = r'ROOT|SBAR|SBARQ|SINV|SQ|S'
    t_PHRASE_POS = r'ADJP|ADVP|CONJP|FRAG|INTJ|LST|NAC|NP|NX|PP|PRN|PRT|QP|RRC|UCP|VP|WHADVP|WHADJP|VHAVP|WHNP|WHPP|X'
    t_WORD_POS = r'CC|CD|DT|EX|FW|IN|JJR|JJS|JJ|LS|MD|NNPS|NNS|NNP|NN|PDT|POS|PRP\$|PRP|RBR|RBS|RB|RP|SYM|TO|UH|VBD|VBG|VBN|VBP|VBZ|VB|WDT|WP\$|WP|WRB|\-LRB\-|\-RRB\-'
    t_PUNCT = r'\.|\,|\:'
    t_TEXT = r'[a-zA-Z-]+'
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
        tree : tree_base
        tree : LPAREN pos tree_contents RPAREN

        """
        if len(p) == 5:
            p[0] = {"pos":p[2], "type" : "pos", "args" : p[3]}
        else:
            p[0] = p[1]

    def p_tree_contents_parse(self, p):
        """
        tree_contents : tree tree_contents
        tree_contents : tree
        """
        if len(p) == 3:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = [p[1]]

    def p_tree_base_parse(self, p):
        """
        tree_base : text_base
        tree_base : dot_base
        """
        p[0] = p[1]

    def p_text_base_parse(self, p):
        """
        text_base : LPAREN pos TEXT RPAREN
        """
        p[0] = {"pos" : p[2], "type" : "text", "args" : [p[3]]}

    def p_dot_base_parse(self, p):
        """
        dot_base : LPAREN PUNCT PUNCT RPAREN
        """
        p[0] = {"pos" : p[2], "type" : "dot", "args" : [p[3]]}

    def p_pos_parse(self, p):
        """
        pos : CLAUSE_POS
        pos : PHRASE_POS
        pos : WORD_POS
        """
        p[0] = p[1]

    def p_error(self, p):
        print "Syntax error at '%s'. Next token: '%s'." % (p.value, ply.yacc.token())

    def parse(self, text):
        print text
        return self.parser.parse(text, lexer=self.lexer)
