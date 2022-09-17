for ((i=0;i<1;i=i+1))
do
echo $i
# c++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) ../C/core/dleft/${i}/Sketches_dleft.cpp -o ../C/core/dleft/${i}/Sketches$(python3-config --extension-suffix)
# c++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) ../C/core/sumax/${i}/Sketches_sumax.cpp -o ../C/core/sumax/${i}/Sketches$(python3-config --extension-suffix)
# c++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) ../C/core/marble/${i}/Sketches_marble.cpp -o ../C/core/marble/${i}/Sketches$(python3-config --extension-suffix)

c++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) ../C/edge/${i}/Sketches_dleft.cpp -o ../C/edge/${i}/Sketches$(python3-config --extension-suffix)

done

# c++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) ../C/time/Sketches_dleft.cpp -o ../C/time/Sketches$(python3-config --extension-suffix)
