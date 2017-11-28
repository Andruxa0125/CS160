#find_library(MGL mgl PATHS /usr/local/lib)
find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})


ADD_EXECUTABLE( eyeLike main.cpp findEyeCenter.cpp findEyeCenter.h findEyeCorner.cpp findEyeCorner.h constants.h helpers.cpp helpers.h)
TARGET_LINK_LIBRARIES( eyeLike ${OpenCV_LIBS} )
#target_link_libraries( eyeLike ${MGL})



ADD_LIBRARY(mylib SHARED wrapper.cpp findEyeCenter.cpp findEyeCenter.h findEyeCorner.cpp findEyeCorner.h constants.h helpers.cpp helpers.h)
TARGET_LINK_LIBRARIES( mylib ${OpenCV_LIBS})

