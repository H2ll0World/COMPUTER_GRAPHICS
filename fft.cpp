#include <iostream>
#include <complex>

#define FFT_COL 8
#define FFT_ROW 16

void transpose(std::vector<std::complex<float> > input[], std::vector<std::complex<float> > output[]){
    for(int i = 0; i < FFT_ROW; i++)
        for(int j = 0; j < FFT_COL; j++)
            output[j][i] = input[i][j];
}

int main(){
    // std::vector<std::complex<float> > data(FFT_SIZE)[16]; // 
    std::vector<std::complex<float>> data[FFT_ROW]; 
    std::vector<std::complex<float>> data2[FFT_COL]; 

    // std::vector<std::vector<std::complex<float>>> transposed(FFT_COL, std::vector<std::complex<float>>(FFT_ROW));

    // 초기화까지 하려면 (각 벡터의 크기를 FFT_SIZE로)
    for(int i = 0; i < FFT_ROW; i++) {
        data[i].resize(FFT_COL);
    }   

    for(int i = 0; i < FFT_COL; i++){
        data2[i].resize(FFT_ROW);
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

    transpose(data, data2);

    for(int i = 0; i < FFT_COL; i++){
        for(int j = 0; j < FFT_ROW; j++)
            std::cout << data2[i][j] << ", ";
        std::cout << "\n";
    }
    std::cout << "\n";


    

    // for(auto iter : data){
    //     std::cout << iter << ' ';
    // }
    // std::complex<float> tmp;
    // data.push_back(tmp);


    return 0;
}
