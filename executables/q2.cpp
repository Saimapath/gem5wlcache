#include<iostream>
#include<vector>
#include<map>
#include<set>
using namespace std;
#define MOD 1000000007
int main(){
    long long n;
    cin>>n;
    vector<long long>dp(n+1);
    dp[0]=1;
    for(long long i=1;i<=n;i++){
        for(int j=1;j<=6; j++){
            if(i-j>=0){
                dp[i]=(dp[i]+dp[i-j])%MOD;
            }
        }
    }
    cout<<dp[n]<<endl;
    return 0;
    

}