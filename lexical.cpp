#include <bits/stdc++.h>
using namespace std;

bool isKeyword(const string &s){
    vector<string> keywords = {"auto", "break", "case", "char", "const", "while", 
                               "endl", "cin", "cout", "string", "sizeof", "continue",
                               "default", "catch", "try", "bool", "using", "sort", 
                               "unsigned", "void", "do", "double", "else", "enum", 
                               "extern", "float", "for", "goto", "typedef", "union",
                               "if", "int", "long", "register", "return", "short", 
                               "signed", "struct", "switch", "static"};
    
    return find(keywords.begin(), keywords.end(), s) != keywords.end();
}

bool isRelational(const string &s){
    vector<string> relop = {">", ">=", "<", "<=", "==", "!="};
    return find(relop.begin(), relop.end(), s) != relop.end();
}

int main(){
    cout << "\n\t\tLexical Analysis\n";
    cout << "_____________________________" << endl << endl;
    
    ifstream fin("input.txt");
    if (!fin.is_open()){
        cout << "File is missing" << endl;
        return 1;
    }

    string keystring = "", opstring = "", idstring = "";
    char ch;

    while (fin.get(ch)){
      
        if (ch == '(' || ch == ')' || ch == '{' || ch == '}' || ch == '[' || ch == ']'){
            cout << "Parenthesis: " << ch << endl;
        }

       
        if (isalpha(ch)){
            keystring += ch;
            idstring += ch;
        } else {
           
            if (!keystring.empty() && isKeyword(keystring)){
                cout << "Keyword: " << keystring << endl;
            }
            keystring.clear();

           
            if (!idstring.empty() && !isKeyword(idstring)){
                cout << "Identifier: " << idstring << endl;
            }
            idstring.clear();
        }

    
        if (ch == '<' || ch == '>' || ch == '=' || ch == '!'){
            opstring += ch;
        } else {
           
            if (!opstring.empty() && isRelational(opstring)){
                cout << "Relational Operator: " << opstring << endl;
            }
            opstring.clear();
        }
    }

    fin.close();
    return 0;
}
