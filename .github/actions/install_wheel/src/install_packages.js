const core = require('@actions/core');
const glob = require('glob');
const path = require('path');
const { exec } = require('child_process');
const util = require('util');

const execAsync = util.promisify(exec);

async function installPackages(packages, localWheelDir, requirementsFiles) {
  core.debug(`Packages to install: ${packages}`);
  core.debug(`Local wheel directory: ${localWheelDir}`);
  core.debug(`Requirements files: ${requirementsFiles}`);

  // Resolve local wheels
  const localWheels = {};
  if (localWheelDir) {
    const wheels = glob.sync(path.posix.join(localWheelDir, '*.whl'));
    core.debug(`Found wheels: ${wheels}`);
    for (const whl of wheels) {
      const packageName = path.basename(whl).split('-')[0];
      localWheels[packageName] = whl;
    }
  }
  core.debug(`Resolved local wheels: ${JSON.stringify(localWheels)}`);

  // Collect wheel paths
  const wheelPaths = [];
  for (const pkg of packages) {
    const packageName = pkg.split('[')[0];
    if (localWheels[packageName]) {
      const wheelPath = localWheels[packageName];
      wheelPaths.push(`"${wheelPath}${pkg.slice(packageName.length)}"`);
    } else {
      core.setFailed(`Package ${pkg} not found locally.`);
      return;
    }
  }
  core.debug(`Collected wheel paths: ${wheelPaths}`);

  // Collect requirements files
  const requirementsArgs = requirementsFiles.map(reqFile => `-r ${reqFile}`);
  core.debug(`Requirements arguments: ${requirementsArgs}`);

  // Install all wheels and requirements in one command
  const installArgs = [...wheelPaths, ...requirementsArgs];
  if (installArgs.length > 0) {
    core.debug(`Installing packages with arguments: ${installArgs.join(' ')}`);
    console.log(`Installing packages: ${installArgs.join(' ')}`);
    const { stdout, stderr } = await execAsync(
      `pip install ${installArgs.join(' ')}`,
      {
        stdio: 'inherit'
      }
    );
    console.log('stdout:', stdout);
    console.error('stderr:', stderr);
  }
}

async function run() {
  try {
    const packagesInput = core.getInput('packages');
    const localWheelDir = core.getInput('local_wheel_dir') || null;
    const requirementsInput = core.getInput('requirements_files') || '';
    const packages = packagesInput.split(';');
    const requirementsFiles = requirementsInput
      .split(';')
      .filter(Boolean)
      .map(reqFile => path.normalize(reqFile));
    const normalizedLocalWheelDir = localWheelDir
      ? path.normalize(localWheelDir)
      : null;
    await installPackages(packages, normalizedLocalWheelDir, requirementsFiles);
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
