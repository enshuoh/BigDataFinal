%{
	#include "scanner.h"
	#include "node.h"
	#include <stdio.h>
	#include <stdlib.h>
	#include <string.h>
	#include <assert.h>
	#include <map>
	#include <vector>
	#include <string>

	using namespace std;
	FILE *fptr;
	int yylex();
	void yyerror(const char *msg);
	void OutPut();
	void EnterScope();
	void ExitScope();
	void Var_Decl();
	void GetVariable();
	void ArrayCalc();
	void EnterWhile();
	void ExitWhile();
	void Logic(const char *logic);
	void Scan();
	void PrintLn();
	void Print();
	
	char Name[50];
	int memory_space;
	Token *TokenNow = NULL;
	Scope *ScopeNow = NULL;
	vector<int> ArraySize; //[10][20][3] a ->stored [3][20][10]
	vector<string> Identifier;
	vector<int> ArithCount;
	char buff_for_itoa[50];
	vector<string> IDName;
	string IDbuff;
	string Buff;
	string ArithBuff;
	int LNow = 0;
	vector<int> L;
	vector<int> InWhileL_Start;
	vector<int> InWhileL_Next;
	vector<string> ScanBuff;
	vector<string> PrintBuff;
	vector<bool> PrintBuffString;
	//#1 for arrayref #2 for in
%}
%union {
	

}
%token INT 262
%token IF 263
%token ELSE 264
%token WHILE 265
%token BREAK 266
%token CONTINUE 267
%token SCAN 268
%token PRINT 269
%token PRINTLN 270
%token ID 271 
%token NUM 272 
%token STRING 273

%right '='
%left "||" 257
%left "&&" 256
%left "==" 260 "!=" 261
%left '<' '>' "<=" 258 ">=" 259
%left '+' '-'
%left '*' '/'
%right POS NEG NOT 
%left '(' ')' '[' ']'

%nonassoc			NO_ELSE		
%nonassoc			ELSE            264

%%
program			:	blockStmt {OutPut();}
				;
//
blockStmt		:	'{' {EnterScope();} varDeclO 
					stmtO {ExitScope();}'}'
				;
varDeclO		:	varDeclO varDecl
				|
				;
stmtO			:	stmtO	stmt
				|
				;
//
varDecl			:	INT {ArraySize.clear();Identifier.clear();} 
					num	ID {Identifier.push_back(TokenNow->token_attr());} 
					idO	';'
					{Var_Decl();}
				;
num				:	num '[' NUM {ArraySize.push_back(atoi(TokenNow->token_attr()));} ']'
				|	
				;
idO				:	idO	','	ID {Identifier.push_back(TokenNow->token_attr());}
				|
				;
//
var				:	ID {
						ArithCount.push_back(0);
						IDbuff="";
						IDbuff+=TokenNow->token_attr();
						IDName.push_back(IDbuff);
						GetVariable();
					} 
					arithExprO 
					{
						ArithCount.pop_back();
						IDName.pop_back();
						ArithBuff+="\tiadd\n";
					}
				;
arithExprO		:	arithExprO '[' 
					{
						ArrayCalc();
						ArithCount.push_back(ArithCount.back()+1);
					}
					arithExpr ']' {ArithBuff+="\tiadd\n";};
				|
				;
//
stmt			:	var '=' arithExpr {Buff+=ArithBuff;ArithBuff.clear(); Buff+="\tiastore\n";} ';' 
				// IF ELSE
				|	IF '(' logicExpr ')' 
					{
						sprintf(buff_for_itoa,"\tifeq L%d\n",LNow);
						L.push_back(LNow+1);
						L.push_back(LNow);
						L.push_back(LNow+1);
						LNow+=2;
						Buff+=buff_for_itoa;
					}
					blockStmt	elseo
				//WHILE
				|	WHILE { EnterWhile(); }
					'(' logicExpr ')' 
					{sprintf(buff_for_itoa,"\tifeq L%d\n",InWhileL_Next.back());Buff+=buff_for_itoa;} //to next
					blockStmt 
					{sprintf(buff_for_itoa,"\tgoto L%d\nL%d:\n",InWhileL_Start.back(),InWhileL_Next.back());Buff+=buff_for_itoa;ExitWhile();}//repeat
				|	BREAK ';' {sprintf(buff_for_itoa,"\tgoto L%d\n",InWhileL_Next.back());Buff+=buff_for_itoa;}
				|	CONTINUE ';' {sprintf(buff_for_itoa,"\tgoto L%d\n",InWhileL_Start.back());Buff+=buff_for_itoa;}
				|	SCAN '(' 
					var {ScanBuff.push_back(ArithBuff);ArithBuff.clear();}
					varO {Scan();}')' ';'
				|	PRINT '(' printableExpr printableExprO ')' ';' {Print();}
				|	PRINTLN '(' printableExpr printableExprO ')' ';'{PrintLn();}
				|	blockStmt
				;
elseo			:
					{
						sprintf(buff_for_itoa,"\tgoto L%d\n",L.back());  //to next
						Buff+=buff_for_itoa;
						L.pop_back();
						sprintf(buff_for_itoa,"L%d:\n",L.back()); //didn't in if stmt
						Buff+=buff_for_itoa;
						L.pop_back();
						sprintf(buff_for_itoa,"\tgoto L%d\n",L.back()); //to next
						Buff+=buff_for_itoa;
						sprintf(buff_for_itoa,"L%d:\n",L.back());
						Buff+=buff_for_itoa;
						L.pop_back();
					}  %prec NO_ELSE   
				|	ELSE
					{
						sprintf(buff_for_itoa,"\tgoto L%d\n",L.back());  //to next
						Buff+=buff_for_itoa;
						L.pop_back();
						sprintf(buff_for_itoa,"L%d:\n",L.back()); //didn't in if stmt
						Buff+=buff_for_itoa;
						L.pop_back();
					}
					blockStmt 
					{
						sprintf(buff_for_itoa,"\tgoto L%d\nL%d:\n",L.back(),L.back()); //to next
						Buff+=buff_for_itoa;
						L.pop_back();
					}
				;
varO			:	varO ',' var {ScanBuff.push_back(ArithBuff);ArithBuff.clear();}
				|
				;
printableExprO	:	printableExprO ',' printableExpr
				|
				;
//
printableExpr	:	STRING {PrintBuff.push_back(string("\tldc \"")+ string(TokenNow->token_attr())+string("\"\n"));PrintBuffString.push_back(true);}
				|	arithExpr{PrintBuff.push_back(ArithBuff);ArithBuff.clear();PrintBuffString.push_back(false);}
				;
//
arithExpr		:	arithExpr '+' arithExpr {ArithBuff += "\tiadd\n";}
				|	arithExpr '-' arithExpr {ArithBuff += "\tisub\n";}
				|	arithExpr '*' arithExpr {ArithBuff += "\timul\n";}
				|	arithExpr '/' arithExpr {ArithBuff += "\tidiv\n";}
				|	'+'	arithExpr %prec POS 
				|	'-'	arithExpr %prec NEG {ArithBuff += "\tineg\n";}
				|	var {ArithBuff += "\tiaload\n";}
				|	NUM {ArithBuff += "\tldc ";ArithBuff += TokenNow->token_attr();ArithBuff +="\n";}
				|	'(' arithExpr ')'
				;
//
logicExpr		:	logicExpr "||" logicExpr {Buff+="\tior\n";}
				|	logicExpr "&&" logicExpr {Buff+="\tiand\n";}
				|	'!' logicExpr {Buff+="\t ldc 1\n\tixor\n";} %prec NOT 
				|	arithExpr{Buff+=ArithBuff;ArithBuff.clear();} '>'  arithExpr {Buff+=ArithBuff;ArithBuff.clear();Logic("if_icmpgt");} 
				|	arithExpr{Buff+=ArithBuff;ArithBuff.clear();} ">=" arithExpr {Buff+=ArithBuff;ArithBuff.clear();Logic("if_icmpge");}
				|	arithExpr{Buff+=ArithBuff;ArithBuff.clear();} '<'  arithExpr {Buff+=ArithBuff;ArithBuff.clear();Logic("if_icmplt");}
				|	arithExpr{Buff+=ArithBuff;ArithBuff.clear();} "<=" arithExpr {Buff+=ArithBuff;ArithBuff.clear();Logic("if_icmple");}
				|	arithExpr{Buff+=ArithBuff;ArithBuff.clear();} "==" arithExpr {Buff+=ArithBuff;ArithBuff.clear();Logic("if_icmpeq");}
				|	arithExpr{Buff+=ArithBuff;ArithBuff.clear();} "!=" arithExpr {Buff+=ArithBuff;ArithBuff.clear();Logic("if_icmpne");}
				|	'[' logicExpr ']'
				;
%%
void OutPut(){
	printf(".import java.io.*\n\n");
	printf(".import java.util.*\n\n");
	printf(".class %s\n\n",Name);
	printf(".method void <init>()\n");
	printf("\taload #0\n");
	printf("\tinvokespecial void <init>() @ Object\n");
	printf("\treturn\n\n");
	printf(".method public static void main(String[])\n");
	printf("\tnew Scanner\n");
	printf("\tdup\n");
	printf("\tgetstatic InputStream in @ System\n");
	printf("\tinvokespecial void <init>(InputStream) @ Scanner\n");
	printf("\tastore #2\n");
	printf("\tldc %d\n",memory_space);
	printf("\tnewarray int\n");
	printf("\tastore #1\n");
	printf("%s",Buff.c_str());
	printf("\treturn\n");
	return;
}
void EnterScope(){
	ScopeNow = new Scope(ScopeNow);
	return;
}
void ExitScope(){
	ScopeNow = ScopeNow->my_parent;
	return;
}
void Var_Decl(){	
	int i,j,size,type = ArraySize.size();
	Variable *var;
	for (i = 0, j = ArraySize.size(),size = 1; i < j; i++)
		size *= ArraySize[i];
	for (i = 0, j= Identifier.size(); i < j; i++){
		var = new Variable;
		var->type = type;
		var->offset = memory_space;
		memory_space += size;
		var->size = ArraySize;
		if(ScopeNow->table.find(Identifier[i]) == ScopeNow->table.end())
			ScopeNow->table.insert(pair<string,Variable>(Identifier[i],*var));
		else
			fprintf(stderr,"repeat variable name : %s\n",Identifier[i].c_str());
	}
	return;
}
void GetVariable(){
	Scope *tmp=ScopeNow;
	map<string,Variable>::iterator it;
	char offset[10]={0};
	while(tmp!=NULL){
		if( (it = tmp->table.find(IDName.back())) != tmp->table.end()){
			sprintf(offset,"%d",it->second.offset);
			break;
		}
		else
			tmp = tmp->my_parent;
	}
	if(tmp == NULL)
		fprintf(stderr,"can't find variable : %s\n",IDName.back().c_str());
		
	ArithBuff+="\taload #1\n";
	ArithBuff+="\tldc ";
	ArithBuff+=offset;
	ArithBuff+="\n";
	ArithBuff+="\tldc 0\n";
	return;
}
void ArrayCalc(){
	Scope *tmp=ScopeNow;
	map<string,Variable>::iterator it;
	ArithBuff+="\tldc ";
	while(tmp!=NULL){
		if( (it = tmp->table.find(IDName.back())) != tmp->table.end())
			break;
		else
			tmp = tmp->my_parent;
	}
	sprintf(buff_for_itoa,"%d\n",tmp->table[IDName.back()].size[ArithCount.back()]);
	ArithBuff+=buff_for_itoa;
	ArithBuff+="\timul\n";
	
	return;
}
void Logic(const char *logic){
	Buff+="\t";
	Buff+=logic;
	sprintf(buff_for_itoa," L%d\n\tldc 0\n\tgoto L%d\n",LNow,LNow+1); //if not true ldc 0
	Buff+=buff_for_itoa;
	sprintf(buff_for_itoa,"L%d:\n\tldc 1\n\tgoto L%d\n",LNow,LNow+1); //if true ldc 1
	Buff+=buff_for_itoa;
	sprintf(buff_for_itoa,"L%d:\n",LNow+1);
	Buff+=buff_for_itoa;
	LNow+=2;
	return;
}
void EnterWhile(){
	sprintf(buff_for_itoa,"L%d:\n",LNow);
	InWhileL_Start.push_back(LNow);
	InWhileL_Next.push_back(LNow+1);
	LNow+=2;
	Buff+=buff_for_itoa;
	return;
}
void ExitWhile(){
	InWhileL_Start.pop_back();
	InWhileL_Next.pop_back();
	return;
}
void Scan(){
	int i,j;
	for(i = 0, j = ScanBuff.size(); i < j ;i++){
		Buff+=ScanBuff[i];
		Buff+="\taload #2\n";
		Buff+="\tinvokevirtual int nextInt() @ Scanner\n";
		Buff+="\tiastore\n";
	}
	ScanBuff.clear();
	return;
}
void PrintLn(){
	int i,j;
	for (i = 0, j = PrintBuff.size(); i < j; i++)
	{
		Buff+="\tgetstatic PrintStream out @ System\n";
		Buff+=PrintBuff[i];
		if(PrintBuffString[i])
			Buff+="\tinvokevirtual void print(String) @ PrintStream\n";
		else
			Buff+="\tinvokevirtual void print(int) @ PrintStream\n";
	}
	Buff+="\tgetstatic PrintStream out @ System\n\tldc \"\\n\"\n\tinvokevirtual void print(String) @ PrintStream\n";
	PrintBuffString.clear();
	PrintBuff.clear();
	return;
}
void Print(){
	int i,j;
	for (i = 0, j = PrintBuff.size(); i < j; i++)
	{
		Buff+="\tgetstatic PrintStream out @ System\n";
		Buff+=PrintBuff[i];
		if(PrintBuffString[i])
			Buff+="\tinvokevirtual void print(String) @ PrintStream\n";
		else
			Buff+="\tinvokevirtual void print(int) @ PrintStream\n";
	}
	PrintBuffString.clear();
	PrintBuff.clear();
	return;
}
int yylex()
{
	TokenNow = Get(fptr);
	if(TokenNow != NULL){
		return TokenNow->token_id();
	}
		return 0;
}
int main(int argc,char* argv[]){
	char *clean;
	fptr = fopen(argv[1],"r");
	strcpy(Name,argv[1]);
	clean = strstr(Name,".cmm");
	*clean = '\0';
	for (int i = 0;; i++){
		Name[i] = Name[i+3];
		if(Name[i+3] == 0)break;
	}

	if(yyparse() == 0){
		fprintf(stderr,"Pass\n");
		return 0;
	}
	else if(yyparse() ==1){
		fprintf(stderr,"Fail\n");
		return 1;
	}
	else{
		fprintf(stderr,"Memexhaust\n");
		return 2;
	}
}
void yyerror(const char *msg){
}