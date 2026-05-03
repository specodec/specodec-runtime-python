import { float32ToString, float64ToString } from './ryu.js';
import * as fs from 'fs';
let passed = 0, total = 0;
// Float32 Original Tests
console.log('=== Float32 Original ===');
const f32Input = fs.readFileSync('../test_cases_f32.txt', 'utf-8').split('\n').filter(l => l.trim() && !l.startsWith('#'));
const f32Expected = fs.readFileSync('../expected_f32.txt', 'utf-8').split('\n').filter(l => l.trim());
passed = 0;
for (let i = 0; i < f32Input.length; i++) {
    const input = parseFloat(f32Input[i]);
    const result = float32ToString(input);
    if (result === f32Expected[i])
        passed++;
    else
        console.log(`FAIL: ${input} => ${result} (expected ${f32Expected[i]})`);
}
total += f32Input.length;
console.log(`${passed}/${f32Input.length}`);
// Float64 Original Tests  
console.log('\n=== Float64 Original ===');
const f64Input = fs.readFileSync('../test_cases_f64.txt', 'utf-8').split('\n').filter(l => l.trim() && !l.startsWith('#'));
const f64Expected = fs.readFileSync('../expected_f64.txt', 'utf-8').split('\n').filter(l => l.trim());
passed = 0;
for (let i = 0; i < f64Input.length; i++) {
    const input = parseFloat(f64Input[i]);
    const result = float64ToString(input);
    if (result === f64Expected[i])
        passed++;
    else if (passed < 5)
        console.log(`FAIL: ${input} => ${result} (expected ${f64Expected[i]})`);
}
total += f64Input.length;
console.log(`${passed}/${f64Input.length}`);
// Float32 Coverage Tests
console.log('\n=== Float32 Coverage ===');
const covInput = fs.readFileSync('../test_cases_table_coverage.txt', 'utf-8').split('\n').filter(l => l.trim() && l[0].match(/\d/));
const covExpected = fs.readFileSync('../expected_table_coverage.txt', 'utf-8').split('\n').filter(l => l.trim());
passed = 0;
for (let i = 0; i < Math.min(covInput.length, covExpected.length); i++) {
    const input = parseFloat(covInput[i].split('#')[0].trim());
    const result = float32ToString(input);
    if (result === covExpected[i])
        passed++;
    else if (passed < 5)
        console.log(`FAIL: ${input} => ${result} (expected ${covExpected[i]})`);
}
total += Math.min(covInput.length, covExpected.length);
console.log(`${passed}/${Math.min(covInput.length, covExpected.length)}`);
// Float64 Coverage Tests
console.log('\n=== Float64 Coverage ===');
const f64CovInput = fs.readFileSync('../test_cases_f64_table_coverage.txt', 'utf-8').split('\n').filter(l => l.trim() && l[0].match(/\d/));
const f64CovExpected = fs.readFileSync('../expected_f64_table_coverage.txt', 'utf-8').split('\n').filter(l => l.trim());
passed = 0;
for (let i = 0; i < Math.min(f64CovInput.length, f64CovExpected.length); i++) {
    const input = parseFloat(f64CovInput[i].split('#')[0].trim());
    const result = float64ToString(input);
    if (result === f64CovExpected[i])
        passed++;
    else if (i < 5)
        console.log(`FAIL: ${input} => ${result} (expected ${f64CovExpected[i]})`);
}
total += Math.min(f64CovInput.length, f64CovExpected.length);
console.log(`${passed}/${Math.min(f64CovInput.length, f64CovExpected.length)}`);
console.log(`\n=== TOTAL: ${total}/920 ===`);
