#include <iostream>

// 송신 Pulse
//    ↓
// 수신 신호
//    ↓
// ADC
//    ↓
// Range FFT
//    ↓
// Doppler FFT
//    ↓
// Range-Doppler Map
//    ↓
// CFAR (Detection)
//    ↓
// 📍 Target Detection List
//    ↓
// 🔥 Tracking (여기서 칼만필터 사용)

#include <iostream>
#include <complex>

#define FFT_COL 8
#define FFT_ROW 16

std::pair<int, int> detection(std::vector<std::complex<float> > input[]){
    

    return std::make_pair(0, 0);
}

int main(){
    std::vector<std::complex<float>> data[FFT_ROW]; 

    // 초기화까지 하려면 (각 벡터의 크기를 FFT_SIZE로)
    for(int i = 0; i < FFT_ROW; i++) {
        data[i].resize(FFT_COL);
    }   

    for(int i = 0; i < FFT_ROW; i++){
        for(int j = 0; j < FFT_COL; j++)
            data[i][j].real(100.0f);
    }

    data[2][4].real(1000.0f);

    for(int i = 0; i < FFT_ROW; i++){
        for(int j = 0; j < FFT_COL; j++)
            std::cout << data[i][j] << ", ";
        std::cout << "\n";
    }
    std::cout << "\n";


    


    return 0;
}
