#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <regex>
#include <algorithm>
#include <map>

using namespace std;

fstream infile_instr;
fstream infile_at;
fstream outfile_dyn;

// Some functions run as application code in Janus may require some maintenance work to be done
// prior to being executed. In order to hide the underlying details of Janus and DynamoRIO,
// the maintenance logic is encapsulated in some helper functions within Janus. The map below
// contains the code that must be inserted prior to any function run by DynamoRIO as application code.
map<string, string> func_name_to_prologue = {
    {
    "run_thread",
    "do_pre_thread_creation_maintenance(janus_context);"
    }
};

map<int, string> num_rule_to_prologue; // Map needed to precompute which function handlers will
// need the additional prologue code; note that this only considers functions from the 
// ".instr" file but not the ".at" file

void compute_num_rule_to_prologue(const string &filename);

int main(int argc, char** argv){
    if(argc < 2){
        cout << "Expecting filename as input" << endl;
        return 1;
    }

    string filename = argv[1];

    compute_num_rule_to_prologue(filename);

    infile_instr.open(filename + ".instr", ios::in);
    infile_at.open(filename + ".at", ios::in);
    outfile_dyn.open(filename + ".dyn", ios::out | ios::trunc);

    int num_rule = 0;
    int num_at_rule = 0;
    string line;
    while(getline(infile_instr, line)){
        if(line != ""){
            if(regex_match(line, regex("func_[0-9]*:"))){
                if(num_rule > 0){
                    outfile_dyn << "}" << endl;
                }
                num_rule++;
                outfile_dyn << "void handler_" + to_string(num_rule) + "(JANUS_CONTEXT){" << endl;
                outfile_dyn << "    instr_t * trigger = get_trigger_instruction(bb,rule);" << endl;
                outfile_dyn << "    uint64_t bitmask = rule->reg1;" << endl;

                const string prologue = num_rule_to_prologue[num_rule];
                if (prologue.size()) {
                    outfile_dyn << "    " + prologue << endl;
                }

                // outfile_dyn << "    int index = get_index_instruction(bb,rule);" << endl;
                continue;
            }
            outfile_dyn << "    " << line << endl;
        }
    }
    while(getline(infile_at, line)){
        if(line != ""){
            if(regex_match(line, regex(".*func_[0-9]*.*"))){
                if(num_rule > 0){
                    outfile_dyn << "}" << endl;
                }
                num_rule++;
                num_at_rule++;
                outfile_dyn << "void handler_" + to_string(num_rule) + "(JANUS_CONTEXT){" << endl;
                outfile_dyn << "    instr_t * trigger = get_trigger_instruction(bb,rule);" << endl;
                outfile_dyn<<  "    dr_ctext = drcontext;"<<endl; 
                outfile_dyn << "    uint64_t bitmask = rule->reg1;" << endl;
                // outfile_dyn << "    int index = get_index_instruction(bb,rule);" << endl;
                continue;
            }
            outfile_dyn << line << endl;
        }
    }
    if(num_rule > 0 && num_at_rule == 0)
        outfile_dyn << "}" << endl;

    outfile_dyn<<"void create_handler_table(){"<<endl;
    
    for(int i=0; i<num_rule; i++){
        outfile_dyn<<"    htable["<<i<<"] = (void*)&handler_"<<i+1<<";"<<endl; 
    }

    outfile_dyn<<"}"<<endl;

    infile_instr.close();
    outfile_dyn.close();

    return 0;
}

void compute_num_rule_to_prologue(const string &filename)
{
    int num_rule = 0;
    string line;

    infile_instr.open(filename + ".instr", ios::in);
    while(getline(infile_instr, line)){
        if(!line.size()) {
            continue;
        }

        if(regex_match(line, regex("func_[0-9]*:"))) {
            num_rule++;
        }
        if(regex_match(line, regex("insert_function_call_as_application.*"))) {
            string prologue;
            for (auto it = func_name_to_prologue.begin(); it != func_name_to_prologue.end(); ++it) {
                const string func_name = it->first;

                if (regex_match(line, regex(".*" + func_name + ".*"))) {
                    prologue = it->second;
                    break;
                }
            }

            if (prologue.size()) {
                num_rule_to_prologue.insert(make_pair(num_rule, prologue));
            }
        }
    }

    infile_instr.close();
}