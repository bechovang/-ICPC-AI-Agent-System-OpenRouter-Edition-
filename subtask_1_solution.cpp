#include <iostream>
#include <vector>
using namespace std;

void fast_io() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
}

int main() {
    fast_io();
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<long long> a(n), b(n);
        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }
        for (int i = 0; i < n; i++) {
            cin >> b[i];
        }

        long long total_positive = 0;
        for (int i = 0; i < n; i++) {
            if (a[i] > b[i]) {
                total_positive += (a[i] - b[i]);
            }
        }

        cout << total_positive + 1 << '\n';
    }
    return 0;
}