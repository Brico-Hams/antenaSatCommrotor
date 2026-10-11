#pragma once
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#define PROGMEM
typedef uint8_t byte;
struct SerialStub{template<class T> void print(T){} template<class T> void println(T){} void println(){} template<class... A> void printf(const char*,A...){}};
static SerialStub Serial;

