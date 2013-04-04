#include<iostream>

using std::cout;
using std::endl;

int main(int argc, char *argv[]) {
    cout << "parametros: ";
    for (int i = 1; i < argc; i++) {
        cout << argv[i] << " ";
    }
    cout << endl;
}
