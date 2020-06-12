import os
from conans import ConanFile, CMake, tools

class SpirvToolsConan(ConanFile):
    name = "spirv-tools"
    version = "2020.3"
    url = "https://github.com/wumo-conan/SPIRV-Tools"
    homepage = "https://github.com/KhronosGroup/SPIRV-Tools/"
    license = "Apache-2.0"

    requires = (
        "effcee/2019.0@wumo/test",
        "glslang/master-tot@wumo/stable",
        "spirv-headers/1.5.3@wumo/test"
    )
    exports_sources = ["CMakeLists.txt", "CONAN_PKG__.patch"]
    generators = "cmake"
    
    settings = "os", "arch", "build_type", "compiler"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, "fPIC": True}
    
    _source_subfolder = "source_subfolder"
    no_copy_source = True
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
    
    def source(self):
        sha256 = "36e0cbd9213109b41bd99134e81a7fc9ffcffced3f9e75ca9db0150da1ebd723"
        tools.get("{}/archive/v{}.zip".format(self.homepage, self.version))
        extracted_folder = f"SPIRV-Tools-{self.version}"
        os.rename(extracted_folder, self._source_subfolder)
    
    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["SPIRV-Headers_SOURCE_DIR"] = self.deps_cpp_info[
            "spirv-headers"].rootpath
        cmake.definitions["SPIRV_SKIP_TESTS"] = True
        cmake.configure()
        return cmake
    
    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
    
    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
    
    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "effcee"
        self.cpp_info.names["cmake_find_package_multi"] = "effcee"
        self.cpp_info.libs = tools.collect_libs(self)
