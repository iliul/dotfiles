openssl pthread math
```
cmake_minimum_required(VERSION 3.6)
project(threaddemo2)
find_library(PTHREAD_LIBRARY pthread)
find_library(MATH_LIBRARY m)
find_library(OPENSSL_LIBRARIES crypto)
set(CMAKE_C_STANDARD 99)
set(SOURCE_FILES test.c)
add_executable(threaddemo2 ${SOURCE_FILES})
target_link_libraries(threaddemo2 ${OPENSSL_LIBRARIES} ${PTHREAD_LIBRARY} ${MATH_LIBRARY} )
```


assembly cmake file
```
cmake_minimum_required(VERSION 3.6)
project(untitled4 C ASM )
set(CMAKE_C_STANDARD 99)
set_source_files_properties(md5-fast-64.S PROPERTIES COMPILE_FLAGS "-x assembler-with-cpp")
set(SOURCE_FILES md5test.c md5-fast-64.S)
add_executable(untitled4 ${SOURCE_FILES})
```
