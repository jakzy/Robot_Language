
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'rightASSIGNMENTleftLESSGREATEREQNOTEQleftPLUSMINUSleftSTARSLASHrightCARETAMPERSAND ASSIGNMENT BLOCK CARET COMMA CONVERSION DATA DECIMAL DOT EQ FALSE FROM GREATER LESS LOGIC L_FBRACKET L_QBRACKET MINUS MOVEDOWN MOVELEFT MOVERIGHT MOVEUP NEWLINE NOTEQ NUMERIC PINGDOWN PINGLEFT PINGRIGHT PINGUP PLUS PROC RECORD R_FBRACKET R_QBRACKET SLASH STAR STRING TEXT TO TRUE UNBLOCK UNDEF VARIABLE VISION VOICEprogram : statementsstatements : statements statement\n                      | statementstatement : declaration NEWLINE\n                     | assignment NEWLINE\n                     | cycle NEWLINE\n                     | command NEWLINE\n                     | procedure NEWLINE\n                     | call NEWLINE\n                     | record NEWLINE\n                     | empty NEWLINEdeclaration : type variableassignment : variable ASSIGNMENT expression\n                      | variable ASSIGNMENT assignment cycle : L_FBRACKET expression R_FBRACKET BLOCK inner_statements UNBLOCKcommand : MOVEUP      L_QBRACKET variable R_QBRACKET\n                   | MOVEDOWN    L_QBRACKET variable R_QBRACKET\n                   | MOVERIGHT   L_QBRACKET variable R_QBRACKET\n                   | MOVELEFT    L_QBRACKET variable R_QBRACKET\n                   | PINGUP      L_QBRACKET variable R_QBRACKET\n                   | PINGDOWN    L_QBRACKET variable R_QBRACKET\n                   | PINGRIGHT   L_QBRACKET variable R_QBRACKET\n                   | PINGLEFT    L_QBRACKET variable R_QBRACKET\n                   | VISION      L_QBRACKET variable R_QBRACKET\n                   | VOICE       L_QBRACKET expression R_QBRACKETprocedure : PROC VARIABLE L_QBRACKET parameters R_QBRACKET statements_groupcall : VARIABLE L_QBRACKET variables R_QBRACKETrecord : RECORD VARIABLE DATA L_QBRACKET parameters R_QBRACKET\n                  | RECORD VARIABLE DATA L_QBRACKET parameters R_QBRACKET conversionsconversions :  conversions conversion\n                       | conversionconversion : CONVERSION TO   type VARIABLE\n                      | CONVERSION FROM type VARIABLEempty : type : NUMERIC\n                | STRING\n                | LOGIC\n                | VARIABLEexpression : variable\n                      | const\n                      | complex_expressionvariables : variables COMMA variable\n                    | variablevariable : VARIABLE L_QBRACKET expression R_QBRACKET\n                    | VARIABLEconst : TRUE\n                 | FALSE\n                 | UNDEF\n                 | DECIMAL\n                 | TEXT\n                 complex_expression : part_expression PLUS    part_expression   %prec PLUS   \n                              | part_expression MINUS   part_expression   %prec MINUS  \n                              | part_expression STAR    part_expression   %prec STAR   \n                              | part_expression SLASH   part_expression   %prec SLASH  \n                              | part_expression CARET   part_expression   %prec CARET  \n                              | part_expression GREATER part_expression   %prec GREATER\n                              | part_expression LESS    part_expression   %prec LESS   \n                              | part_expression EQ      part_expression   %prec EQ     \n                              | part_expression NOTEQ   part_expression   %prec NOTEQ  \n                              | MINUS expressionpart_expression : DOT expressionpart_expression : expression DOTpart_expression : expressionparameters : parameter COMMA parameters\n                      | parameterparameter : type VARIABLE AMPERSAND\n                     | type VARIABLEstatements_group : BLOCK inner_statements UNBLOCK\n                            | inner_statementinner_statements :  inner_statement inner_statements\n                            | inner_statementinner_statement : declaration NEWLINE\n                     | assignment NEWLINE\n                     | cycle NEWLINE\n                     | command NEWLINE\n                     | call NEWLINE\n                     | empty NEWLINEstatement : errors NEWLINEstatement : errorserrors : errors error\n        | error'
    
_lr_action_items = {'L_FBRACKET':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,104,134,141,148,149,150,151,152,153,155,],[15,15,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,15,15,15,-72,-73,-74,-75,-76,-77,15,]),'MOVEUP':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,104,134,141,148,149,150,151,152,153,155,],[16,16,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,16,16,16,-72,-73,-74,-75,-76,-77,16,]),'MOVEDOWN':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,104,134,141,148,149,150,151,152,153,155,],[17,17,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,17,17,17,-72,-73,-74,-75,-76,-77,17,]),'MOVERIGHT':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,104,134,141,148,149,150,151,152,153,155,],[18,18,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,18,18,18,-72,-73,-74,-75,-76,-77,18,]),'MOVELEFT':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,104,134,141,148,149,150,151,152,153,155,],[19,19,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,19,19,19,-72,-73,-74,-75,-76,-77,19,]),'PINGUP':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,104,134,141,148,149,150,151,152,153,155,],[20,20,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,20,20,20,-72,-73,-74,-75,-76,-77,20,]),'PINGDOWN':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,104,134,141,148,149,150,151,152,153,155,],[21,21,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,21,21,21,-72,-73,-74,-75,-76,-77,21,]),'PINGRIGHT':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,104,134,141,148,149,150,151,152,153,155,],[22,22,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,22,22,22,-72,-73,-74,-75,-76,-77,22,]),'PINGLEFT':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,104,134,141,148,149,150,151,152,153,155,],[23,23,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,23,23,23,-72,-73,-74,-75,-76,-77,23,]),'VISION':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,104,134,141,148,149,150,151,152,153,155,],[24,24,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,24,24,24,-72,-73,-74,-75,-76,-77,24,]),'VOICE':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,104,134,141,148,149,150,151,152,153,155,],[25,25,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,25,25,25,-72,-73,-74,-75,-76,-77,25,]),'PROC':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,],[26,26,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,]),'VARIABLE':([0,2,3,12,13,15,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,46,57,58,59,60,61,62,63,64,65,66,67,68,70,72,78,79,80,81,82,83,84,85,86,99,104,125,128,130,132,134,141,142,148,149,150,151,152,153,155,166,167,168,169,],[27,27,-3,-79,45,45,69,-38,71,-81,-35,-36,-37,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,125,27,-38,143,45,125,27,27,125,-72,-73,-74,-75,-76,-77,27,125,125,170,171,]),'RECORD':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,],[28,28,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,]),'NEWLINE':([0,2,3,4,5,6,7,8,9,10,11,12,29,33,34,35,36,37,38,39,40,41,42,43,44,45,48,49,50,51,52,53,54,55,73,74,75,77,87,88,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,129,131,134,135,136,137,138,139,140,141,146,148,149,150,151,152,153,154,155,156,159,161,162,164,165,170,171,],[-34,-34,-3,34,35,36,37,38,39,40,41,42,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,-12,-45,-39,-40,-41,-46,-47,-48,-49,-50,-39,-13,-14,-62,-60,-61,-34,-51,-63,-52,-53,-54,-55,-56,-57,-58,-59,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-27,-44,-34,148,149,150,151,152,153,-34,-15,-72,-73,-74,-75,-76,-77,-26,-34,-69,-28,-29,-31,-68,-30,-32,-33,]),'error':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,],[29,29,-3,43,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,]),'NUMERIC':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,99,104,132,134,141,142,148,149,150,151,152,153,155,166,167,],[30,30,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,30,30,30,30,30,30,-72,-73,-74,-75,-76,-77,30,30,30,]),'STRING':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,99,104,132,134,141,142,148,149,150,151,152,153,155,166,167,],[31,31,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,31,31,31,31,31,31,-72,-73,-74,-75,-76,-77,31,31,31,]),'LOGIC':([0,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,99,104,132,134,141,142,148,149,150,151,152,153,155,166,167,],[32,32,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,32,32,32,32,32,32,-72,-73,-74,-75,-76,-77,32,32,32,]),'$end':([1,2,3,12,29,33,34,35,36,37,38,39,40,41,42,43,],[0,-1,-3,-79,-81,-2,-4,-5,-6,-7,-8,-9,-10,-11,-78,-80,]),'ASSIGNMENT':([14,27,45,73,131,],[46,-45,-45,46,-44,]),'TRUE':([15,46,57,58,68,70,72,78,79,80,81,82,83,84,85,86,],[51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,]),'FALSE':([15,46,57,58,68,70,72,78,79,80,81,82,83,84,85,86,],[52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,]),'UNDEF':([15,46,57,58,68,70,72,78,79,80,81,82,83,84,85,86,],[53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,]),'DECIMAL':([15,46,57,58,68,70,72,78,79,80,81,82,83,84,85,86,],[54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,]),'TEXT':([15,46,57,58,68,70,72,78,79,80,81,82,83,84,85,86,],[55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,]),'MINUS':([15,45,46,47,48,49,50,51,52,53,54,55,56,57,58,68,70,72,73,74,77,78,79,80,81,82,83,84,85,86,87,88,98,101,102,105,106,107,108,109,110,111,112,113,114,131,],[57,-45,57,-63,-39,-40,-41,-46,-47,-48,-49,-50,79,57,57,57,57,57,-39,-63,-62,57,57,57,57,57,57,57,57,57,-60,-61,-63,-63,-39,-51,-63,-52,-53,-54,-55,79,79,79,79,-44,]),'DOT':([15,45,46,47,48,49,50,51,52,53,54,55,57,58,68,70,72,73,74,77,78,79,80,81,82,83,84,85,86,87,88,98,101,102,105,106,107,108,109,110,111,112,113,114,131,],[58,-45,58,77,-39,-40,-41,-46,-47,-48,-49,-50,58,58,58,58,58,-39,77,-62,58,58,58,58,58,58,58,58,58,-60,77,77,77,-39,-51,77,-52,-53,-54,-55,-56,-57,-58,-59,-44,]),'L_QBRACKET':([16,17,18,19,20,21,22,23,24,25,27,45,69,103,],[59,60,61,62,63,64,65,66,67,68,70,72,99,132,]),'R_FBRACKET':([45,47,48,49,50,51,52,53,54,55,77,87,88,105,106,107,108,109,110,111,112,113,114,131,],[-45,76,-39,-40,-41,-46,-47,-48,-49,-50,-62,-60,-61,-51,-63,-52,-53,-54,-55,-56,-57,-58,-59,-44,]),'PLUS':([45,47,48,49,50,51,52,53,54,55,56,73,74,77,87,88,98,101,102,105,106,107,108,109,110,111,112,113,114,131,],[-45,-63,-39,-40,-41,-46,-47,-48,-49,-50,78,-39,-63,-62,-60,-61,-63,-63,-39,-51,-63,-52,-53,-54,-55,78,78,78,78,-44,]),'STAR':([45,47,48,49,50,51,52,53,54,55,56,73,74,77,87,88,98,101,102,105,106,107,108,109,110,111,112,113,114,131,],[-45,-63,-39,-40,-41,-46,-47,-48,-49,-50,80,-39,-63,-62,-60,-61,-63,-63,-39,80,-63,80,-53,-54,-55,80,80,80,80,-44,]),'SLASH':([45,47,48,49,50,51,52,53,54,55,56,73,74,77,87,88,98,101,102,105,106,107,108,109,110,111,112,113,114,131,],[-45,-63,-39,-40,-41,-46,-47,-48,-49,-50,81,-39,-63,-62,-60,-61,-63,-63,-39,81,-63,81,-53,-54,-55,81,81,81,81,-44,]),'CARET':([45,47,48,49,50,51,52,53,54,55,56,73,74,77,87,88,98,101,102,105,106,107,108,109,110,111,112,113,114,131,],[-45,-63,-39,-40,-41,-46,-47,-48,-49,-50,82,-39,-63,-62,-60,-61,-63,-63,-39,82,-63,82,82,82,82,82,82,82,82,-44,]),'GREATER':([45,47,48,49,50,51,52,53,54,55,56,73,74,77,87,88,98,101,102,105,106,107,108,109,110,111,112,113,114,131,],[-45,-63,-39,-40,-41,-46,-47,-48,-49,-50,83,-39,-63,-62,-60,-61,-63,-63,-39,-51,-63,-52,-53,-54,-55,-56,-57,-58,-59,-44,]),'LESS':([45,47,48,49,50,51,52,53,54,55,56,73,74,77,87,88,98,101,102,105,106,107,108,109,110,111,112,113,114,131,],[-45,-63,-39,-40,-41,-46,-47,-48,-49,-50,84,-39,-63,-62,-60,-61,-63,-63,-39,-51,-63,-52,-53,-54,-55,-56,-57,-58,-59,-44,]),'EQ':([45,47,48,49,50,51,52,53,54,55,56,73,74,77,87,88,98,101,102,105,106,107,108,109,110,111,112,113,114,131,],[-45,-63,-39,-40,-41,-46,-47,-48,-49,-50,85,-39,-63,-62,-60,-61,-63,-63,-39,-51,-63,-52,-53,-54,-55,-56,-57,-58,-59,-44,]),'NOTEQ':([45,47,48,49,50,51,52,53,54,55,56,73,74,77,87,88,98,101,102,105,106,107,108,109,110,111,112,113,114,131,],[-45,-63,-39,-40,-41,-46,-47,-48,-49,-50,86,-39,-63,-62,-60,-61,-63,-63,-39,-51,-63,-52,-53,-54,-55,-56,-57,-58,-59,-44,]),'R_QBRACKET':([45,48,49,50,51,52,53,54,55,77,87,88,89,90,91,92,93,94,95,96,97,98,100,101,102,105,106,107,108,109,110,111,112,113,114,126,127,131,143,144,145,157,158,],[-45,-39,-40,-41,-46,-47,-48,-49,-50,-62,-60,-61,115,116,117,118,119,120,121,122,123,124,129,131,-39,-51,-63,-52,-53,-54,-55,-56,-57,-58,-59,141,-65,-44,-67,-42,159,-64,-66,]),'COMMA':([45,100,102,127,131,143,144,158,],[-45,130,-43,142,-44,-67,-42,-66,]),'DATA':([71,],[103,]),'BLOCK':([76,141,],[104,155,]),'UNBLOCK':([133,134,147,148,149,150,151,152,153,160,],[146,-71,-70,-72,-73,-74,-75,-76,-77,164,]),'AMPERSAND':([143,],[158,]),'CONVERSION':([159,161,162,165,170,171,],[163,163,-31,-30,-32,-33,]),'TO':([163,],[166,]),'FROM':([163,],[167,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'statements':([0,],[2,]),'statement':([0,2,],[3,33,]),'declaration':([0,2,104,134,141,155,],[4,4,135,135,135,135,]),'assignment':([0,2,46,104,134,141,155,],[5,5,75,136,136,136,136,]),'cycle':([0,2,104,134,141,155,],[6,6,137,137,137,137,]),'command':([0,2,104,134,141,155,],[7,7,138,138,138,138,]),'procedure':([0,2,],[8,8,]),'call':([0,2,104,134,141,155,],[9,9,139,139,139,139,]),'record':([0,2,],[10,10,]),'empty':([0,2,104,134,141,155,],[11,11,140,140,140,140,]),'errors':([0,2,],[12,12,]),'type':([0,2,99,104,132,134,141,142,155,166,167,],[13,13,128,13,128,13,13,128,13,168,169,]),'variable':([0,2,13,15,46,57,58,59,60,61,62,63,64,65,66,67,68,70,72,78,79,80,81,82,83,84,85,86,104,130,134,141,155,],[14,14,44,48,73,48,48,89,90,91,92,93,94,95,96,97,48,102,48,48,48,48,48,48,48,48,48,48,14,144,14,14,14,]),'expression':([15,46,57,58,68,70,72,78,79,80,81,82,83,84,85,86,],[47,74,87,88,98,101,101,106,106,106,106,106,106,106,106,106,]),'const':([15,46,57,58,68,70,72,78,79,80,81,82,83,84,85,86,],[49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,]),'complex_expression':([15,46,57,58,68,70,72,78,79,80,81,82,83,84,85,86,],[50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,]),'part_expression':([15,46,57,58,68,70,72,78,79,80,81,82,83,84,85,86,],[56,56,56,56,56,56,56,105,107,108,109,110,111,112,113,114,]),'variables':([70,],[100,]),'parameters':([99,132,142,],[126,145,157,]),'parameter':([99,132,142,],[127,127,127,]),'inner_statements':([104,134,155,],[133,147,160,]),'inner_statement':([104,134,141,155,],[134,134,156,134,]),'statements_group':([141,],[154,]),'conversions':([159,],[161,]),'conversion':([159,161,],[162,165,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statements','program',1,'p_program','parser.py',31),
  ('statements -> statements statement','statements',2,'p_statements','parser.py',36),
  ('statements -> statement','statements',1,'p_statements','parser.py',37),
  ('statement -> declaration NEWLINE','statement',2,'p_statement','parser.py',45),
  ('statement -> assignment NEWLINE','statement',2,'p_statement','parser.py',46),
  ('statement -> cycle NEWLINE','statement',2,'p_statement','parser.py',47),
  ('statement -> command NEWLINE','statement',2,'p_statement','parser.py',48),
  ('statement -> procedure NEWLINE','statement',2,'p_statement','parser.py',49),
  ('statement -> call NEWLINE','statement',2,'p_statement','parser.py',50),
  ('statement -> record NEWLINE','statement',2,'p_statement','parser.py',51),
  ('statement -> empty NEWLINE','statement',2,'p_statement','parser.py',52),
  ('declaration -> type variable','declaration',2,'p_declaration','parser.py',57),
  ('assignment -> variable ASSIGNMENT expression','assignment',3,'p_assignment','parser.py',62),
  ('assignment -> variable ASSIGNMENT assignment','assignment',3,'p_assignment','parser.py',63),
  ('cycle -> L_FBRACKET expression R_FBRACKET BLOCK inner_statements UNBLOCK','cycle',6,'p_cycle','parser.py',68),
  ('command -> MOVEUP L_QBRACKET variable R_QBRACKET','command',4,'p_command','parser.py',73),
  ('command -> MOVEDOWN L_QBRACKET variable R_QBRACKET','command',4,'p_command','parser.py',74),
  ('command -> MOVERIGHT L_QBRACKET variable R_QBRACKET','command',4,'p_command','parser.py',75),
  ('command -> MOVELEFT L_QBRACKET variable R_QBRACKET','command',4,'p_command','parser.py',76),
  ('command -> PINGUP L_QBRACKET variable R_QBRACKET','command',4,'p_command','parser.py',77),
  ('command -> PINGDOWN L_QBRACKET variable R_QBRACKET','command',4,'p_command','parser.py',78),
  ('command -> PINGRIGHT L_QBRACKET variable R_QBRACKET','command',4,'p_command','parser.py',79),
  ('command -> PINGLEFT L_QBRACKET variable R_QBRACKET','command',4,'p_command','parser.py',80),
  ('command -> VISION L_QBRACKET variable R_QBRACKET','command',4,'p_command','parser.py',81),
  ('command -> VOICE L_QBRACKET expression R_QBRACKET','command',4,'p_command','parser.py',82),
  ('procedure -> PROC VARIABLE L_QBRACKET parameters R_QBRACKET statements_group','procedure',6,'p_procedure','parser.py',87),
  ('call -> VARIABLE L_QBRACKET variables R_QBRACKET','call',4,'p_call','parser.py',92),
  ('record -> RECORD VARIABLE DATA L_QBRACKET parameters R_QBRACKET','record',6,'p_record','parser.py',97),
  ('record -> RECORD VARIABLE DATA L_QBRACKET parameters R_QBRACKET conversions','record',7,'p_record','parser.py',98),
  ('conversions -> conversions conversion','conversions',2,'p_conversions','parser.py',106),
  ('conversions -> conversion','conversions',1,'p_conversions','parser.py',107),
  ('conversion -> CONVERSION TO type VARIABLE','conversion',4,'p_conversion','parser.py',115),
  ('conversion -> CONVERSION FROM type VARIABLE','conversion',4,'p_conversion','parser.py',116),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',121),
  ('type -> NUMERIC','type',1,'p_type','parser.py',126),
  ('type -> STRING','type',1,'p_type','parser.py',127),
  ('type -> LOGIC','type',1,'p_type','parser.py',128),
  ('type -> VARIABLE','type',1,'p_type','parser.py',129),
  ('expression -> variable','expression',1,'p_expression','parser.py',134),
  ('expression -> const','expression',1,'p_expression','parser.py',135),
  ('expression -> complex_expression','expression',1,'p_expression','parser.py',136),
  ('variables -> variables COMMA variable','variables',3,'p_variables','parser.py',141),
  ('variables -> variable','variables',1,'p_variables','parser.py',142),
  ('variable -> VARIABLE L_QBRACKET expression R_QBRACKET','variable',4,'p_variable','parser.py',150),
  ('variable -> VARIABLE','variable',1,'p_variable','parser.py',151),
  ('const -> TRUE','const',1,'p_const','parser.py',159),
  ('const -> FALSE','const',1,'p_const','parser.py',160),
  ('const -> UNDEF','const',1,'p_const','parser.py',161),
  ('const -> DECIMAL','const',1,'p_const','parser.py',162),
  ('const -> TEXT','const',1,'p_const','parser.py',163),
  ('complex_expression -> part_expression PLUS part_expression','complex_expression',3,'p_complex_expression','parser.py',169),
  ('complex_expression -> part_expression MINUS part_expression','complex_expression',3,'p_complex_expression','parser.py',170),
  ('complex_expression -> part_expression STAR part_expression','complex_expression',3,'p_complex_expression','parser.py',171),
  ('complex_expression -> part_expression SLASH part_expression','complex_expression',3,'p_complex_expression','parser.py',172),
  ('complex_expression -> part_expression CARET part_expression','complex_expression',3,'p_complex_expression','parser.py',173),
  ('complex_expression -> part_expression GREATER part_expression','complex_expression',3,'p_complex_expression','parser.py',174),
  ('complex_expression -> part_expression LESS part_expression','complex_expression',3,'p_complex_expression','parser.py',175),
  ('complex_expression -> part_expression EQ part_expression','complex_expression',3,'p_complex_expression','parser.py',176),
  ('complex_expression -> part_expression NOTEQ part_expression','complex_expression',3,'p_complex_expression','parser.py',177),
  ('complex_expression -> MINUS expression','complex_expression',2,'p_complex_expression','parser.py',178),
  ('part_expression -> DOT expression','part_expression',2,'p_part_expression_right','parser.py',186),
  ('part_expression -> expression DOT','part_expression',2,'p_part_expression_left','parser.py',191),
  ('part_expression -> expression','part_expression',1,'p_part_expression','parser.py',196),
  ('parameters -> parameter COMMA parameters','parameters',3,'p_parameters','parser.py',201),
  ('parameters -> parameter','parameters',1,'p_parameters','parser.py',202),
  ('parameter -> type VARIABLE AMPERSAND','parameter',3,'p_parameter','parser.py',210),
  ('parameter -> type VARIABLE','parameter',2,'p_parameter','parser.py',211),
  ('statements_group -> BLOCK inner_statements UNBLOCK','statements_group',3,'p_statements_group','parser.py',219),
  ('statements_group -> inner_statement','statements_group',1,'p_statements_group','parser.py',220),
  ('inner_statements -> inner_statement inner_statements','inner_statements',2,'p_inner_statements','parser.py',228),
  ('inner_statements -> inner_statement','inner_statements',1,'p_inner_statements','parser.py',229),
  ('inner_statement -> declaration NEWLINE','inner_statement',2,'p_inner_statement','parser.py',237),
  ('inner_statement -> assignment NEWLINE','inner_statement',2,'p_inner_statement','parser.py',238),
  ('inner_statement -> cycle NEWLINE','inner_statement',2,'p_inner_statement','parser.py',239),
  ('inner_statement -> command NEWLINE','inner_statement',2,'p_inner_statement','parser.py',240),
  ('inner_statement -> call NEWLINE','inner_statement',2,'p_inner_statement','parser.py',241),
  ('inner_statement -> empty NEWLINE','inner_statement',2,'p_inner_statement','parser.py',242),
  ('statement -> errors NEWLINE','statement',2,'p_statement_error','parser.py',247),
  ('statement -> errors','statement',1,'p_statement_error_no_nl','parser.py',252),
  ('errors -> errors error','errors',2,'p_errors','parser.py',257),
  ('errors -> error','errors',1,'p_errors','parser.py',258),
]
