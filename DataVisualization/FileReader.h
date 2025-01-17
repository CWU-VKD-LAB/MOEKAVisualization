#pragma once
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include "UI/Function.h"
#include "UI/Form.h"


class CSVReader {
private:
	static void saveFunction(std::ofstream& file, Function* func, int depth);
public:
	static std::vector<Function*> loadedFunctionHistory;
	static void readCSV(std::vector<Function*>* container, std::string path);
	static void saveToCSV(std::vector<Function*>* data, std::string path);
};
