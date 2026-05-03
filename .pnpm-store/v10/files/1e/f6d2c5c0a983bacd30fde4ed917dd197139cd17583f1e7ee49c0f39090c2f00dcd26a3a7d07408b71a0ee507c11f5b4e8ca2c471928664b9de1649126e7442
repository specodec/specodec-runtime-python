import { execSync } from 'child_process';
import { existsSync, mkdirSync, rmSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dir = dirname(fileURLToPath(import.meta.url));
const LANG_ROOT = join(__dir, '..');
const TESTS_DIR = __dir;
const CACHE = join(TESTS_DIR, '.tests-cache');
const PROXY = process.env.PROXY || 'http://127.0.0.1:17890';

const BUILD_ARGS = `--build-arg HTTP_PROXY=${PROXY} --build-arg HTTPS_PROXY=${PROXY} --build-arg http_proxy=${PROXY} --build-arg https_proxy=${PROXY} --build-arg ALL_PROXY=${PROXY} --build-arg all_proxy=${PROXY}`;
const COMMON = `--network host ${BUILD_ARGS}`;

function run(cmd: string) {
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

const vectorsDir = join(CACHE, 'vectors');
const goldenDir = join(CACHE, 'golden');

// Step 2: Self-check golden
console.log('\n=== Step 2: Golden self-check ===');
run(`cd ${CACHE} && npx tsx verify.ts`);

// Step 3: Runtime roundtrip test
console.log('\n=== Step 3: Runtime roundtrip test ===');
const outputDir = join(TESTS_DIR, 'output');
if (existsSync(outputDir)) rmSync(outputDir, { recursive: true });
mkdirSync(join(outputDir, 'scalars'), { recursive: true });

run(`cd ${TESTS_DIR} && podman build ${COMMON} -t specodec-interop-ts -f Containerfile \
  --build-context specodec-runtime-ts=${LANG_ROOT} \
  --build-context run=${TESTS_DIR}/run \
  --build-context vectors=${vectorsDir} .`);

const container = execSync(`podman create specodec-interop-ts /bin/true`).toString().trim();
run(`podman cp ${container}:/app/output/. ${outputDir}/`);
run(`podman rm ${container}`);

// Step 4: Verify runtime output
console.log('\n=== Step 4: Verify runtime output ===');
run(`cd ${CACHE} && npx tsx verify.ts --output ${outputDir} --golden ${goldenDir}`);

// Step 5: Emit test
console.log('\n=== Step 5: Emit roundtrip test ===');
const emitGen = join(TESTS_DIR, '.emit-gen');
if (existsSync(emitGen)) rmSync(emitGen, { recursive: true });
mkdirSync(emitGen, { recursive: true });

run(`cd ${LANG_ROOT} && npx tsp compile ${CACHE}/alltypes.tsp --emit=@specodec/typespec-emitter-ts \
  --option @specodec/typespec-emitter-ts.emitter-output-dir=${emitGen}`);

const outputEmit = join(TESTS_DIR, 'output_emit');
if (existsSync(outputEmit)) rmSync(outputEmit, { recursive: true });
mkdirSync(outputEmit, { recursive: true });

run(`cd ${TESTS_DIR} && podman build ${COMMON} -t specodec-emit-ts -f Containerfile.emit \
  --build-context specodec-runtime-ts=${LANG_ROOT} \
  --build-context emit=${TESTS_DIR}/emit \
  --build-context emit_gen=${emitGen} \
  --build-context vectors=${vectorsDir} .`);

const container2 = execSync(`podman create specodec-emit-ts /bin/true`).toString().trim();
run(`podman cp ${container2}:/app/output_emit/. ${outputEmit}/`);
run(`podman rm ${container2}`);

// Step 6: Verify emit output (TODO: verify_emit.ts)
console.log('\n=== Step 6: Verify emit output ===');
console.log('  (skipped - verify_emit.ts not yet implemented)');

console.log('\n=== ALL PASSED ===');