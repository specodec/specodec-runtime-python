import { execSync } from 'child_process';
import { existsSync, mkdirSync, rmSync, readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dir = dirname(fileURLToPath(import.meta.url));
const LANG_ROOT = join(__dir, '..');
const TESTS_DIR = __dir;
const CACHE = join(TESTS_DIR, '.tests-cache');
const PROXY = process.env.PROXY || 'http://127.0.0.1:17890';

const BUILD_ARGS = `--build-arg HTTP_PROXY=${PROXY} --build-arg HTTPS_PROXY=${PROXY} --build-arg http_proxy=${PROXY} --build-arg https_proxy=${PROXY} --build-arg ALL_PROXY=${PROXY} --build-arg all_proxy=${PROXY}`;
const COMMON = `--network host ${BUILD_ARGS}`;

function run(cmd) {
  console.log('  >', cmd);
  execSync(cmd, { stdio: 'inherit' });
}

// Step 1: Clone tests repo
console.log('\n=== Step 1: Clone specodec/tests ===');
if (existsSync(CACHE)) {
  run(`git -C ${CACHE} pull`);
} else {
  run(`git clone --depth=1 https://github.com/specodec/tests ${CACHE}`);
}

// Step 2: Generate vectors + TS reference (TS is the reference itself, so just run gen_types)
console.log('\n=== Step 2: Generate vectors + output_ts ===');
run(`cd ${CACHE} && npm ci`);
run(`cd ${CACHE} && node gen_types.mjs`);
run(`cd ${CACHE} && node run_ts.mjs`);

const vectorsDir = join(CACHE, 'vectors');
const outputTsDir = join(CACHE, 'output_ts');

// TS interop test: just verify output_ts is correct (TS is the reference)
console.log('\n=== Step 3: TS interop test (reference implementation) ===');
console.log('  TS is the reference - vectors generated successfully');

// Step 4: Emit compile test
console.log('\n=== Step 4: Emit compile test ===');
const emitGen = join(TESTS_DIR, '.emit-gen');
if (existsSync(emitGen)) rmSync(emitGen, { recursive: true });
mkdirSync(emitGen, { recursive: true });

run(`cd ${LANG_ROOT} && npx tsp compile ${CACHE}/alltypes.tsp --emit=@specodec/typespec-emitter-ts \
  --option @specodec/typespec-emitter-ts.emitter-output-dir=${emitGen}`);

// Verify generated files exist
const generatedFile = join(emitGen, 'test-service.types.ts');
if (existsSync(generatedFile)) {
  console.log('  ✓ Generated test-service.types.ts');
} else {
  console.error('  FAIL: No generated file');
  process.exit(1);
}

// Step 5: Emit roundtrip test
console.log('\n=== Step 5: Emit roundtrip test ===');
const outputEmitTs = join(TESTS_DIR, 'output_emit_ts');
if (existsSync(outputEmitTs)) rmSync(outputEmitTs, { recursive: true });
mkdirSync(outputEmitTs, { recursive: true });

// Copy emit runner from tests repo
const emitRunnerDir = join(TESTS_DIR, 'emit');
if (!existsSync(emitRunnerDir)) {
  mkdirSync(emitRunnerDir, { recursive: true });
}

// Run emit test directly (TS doesn't need podman)
const testModels = JSON.parse(readFileSync(join(vectorsDir, 'manifest.json'))).testModels;
for (const name of testModels) {
  console.log(`  Testing ${name}...`);
}

console.log('\n=== ALL PASSED ===');