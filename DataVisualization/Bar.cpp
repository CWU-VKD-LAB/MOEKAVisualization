#include "Bar.h"

// this is useful so we don't get the out of bounds issue when someone uses N/A as the class choice
ImVec4 INVALID_COLOR = ImVec4(0.0f, 0.0f, 0.0f, 1.0f);

// creates a bar object that stores its class value and color.
Bar::Bar(int classValue, std::vector<int>* p, float width, float height) : Shape{width, height} {
	
	classVal = classValue;
	// if classVal = -1, we are going to use black or some placeholder color for NA color. 
	color = (classVal == -1) ? &INVALID_COLOR : &config::classColors[classVal];
	datapoint = *p;
	
	// shape.h field that tells us if the shape is a bar. yes, it looks dumb, but it was an easier than
	// dealing with casting pointers and such.
	isBar = true;
}

// draw the bar using individual color or class color.
void Bar::draw() {
	if (useIndividualColor) {
		color = &individualColor;
	}
	else {
		// if classVal = -1, we are going to use black or some placeholder color for NA color. 
		color = (classVal == -1) ? &INVALID_COLOR : &config::classColors[classVal];
	}
	bind();
	GLCall(glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr));
}
