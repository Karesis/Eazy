; ModuleID = "eazy_module"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare i32 @"printf"(i8* %".1", ...)

@".str.int_format" = internal constant [4 x i8] c"%d\0a\00"
define i32 @"main"()
{
entry:
  %"x" = alloca i32
  store i32 5, i32* %"x"
  %".3" = bitcast [4 x i8]* @".str.int_format" to i8*
  %"printf_call" = call i32 (i8*, ...) @"printf"(i8* %".3", i32 100)
  %"x_val" = load i32, i32* %"x"
  %"cmp_gt" = icmp sgt i32 %"x_val", 0
  br i1 %"cmp_gt", label %"thenLabel", label %"else_after_if_thenLabel"
thenLabel:
  %".6" = bitcast [4 x i8]* @".str.int_format" to i8*
  %"printf_call.1" = call i32 (i8*, ...) @"printf"(i8* %".6", i32 300)
  %".7" = bitcast [4 x i8]* @".str.int_format" to i8*
  %"printf_call.2" = call i32 (i8*, ...) @"printf"(i8* %".7", i32 400)
  %"x_val.1" = load i32, i32* %"x"
  %"cmp_gt.1" = icmp sgt i32 %"x_val.1", 0
  br i1 %"cmp_gt.1", label %"anotherThen", label %"else_after_if_anotherThen"
else_after_if_thenLabel:
  br label %"thenLabel"
anotherThen:
  %".10" = bitcast [4 x i8]* @".str.int_format" to i8*
  %"printf_call.3" = call i32 (i8*, ...) @"printf"(i8* %".10", i32 600)
  %".11" = bitcast [4 x i8]* @".str.int_format" to i8*
  %"printf_call.4" = call i32 (i8*, ...) @"printf"(i8* %".11", i32 700)
  ret i32 0
else_after_if_anotherThen:
  br label %"anotherThen"
}
