#include<iostream>
#include<vector>
using namespace std;


int main(){
    long long t;cin>>t;
    while(t!=1){
        cout<<t<<" ";
        if(t%2==1){
            t*=3;
            t++;
        }
        else{
            t/=2;
        }

    }
    cout<<1;
}
