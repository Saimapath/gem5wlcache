#include <iostream>
using namespace std;

class GFG {
public:
    void call_Function() // function that calls print
    {
        print();
    }
    void print() // the display function
    {
        cout << "Printing the Base class Content" << endl;
    }
};

class GFG2 : public GFG // GFG2 inherits publicly from GFG
{
public:
    void printing() // GFG2's display
    {
        cout << "Printing the Derived class Content" << endl;
    }
};

int main()
{
    GFG* geeksforgeeks = new GFG(); // Creating GFG's object using pointer
    geeksforgeeks->print(); // Calling call_Function

    GFG* geeksforgeeks2 = new GFG2(); // creating GFG2 object using pointer
    geeksforgeeks2->print(); // calling call_Function for GFG2 object

    delete geeksforgeeks;
    delete geeksforgeeks2;

    return 0;
}