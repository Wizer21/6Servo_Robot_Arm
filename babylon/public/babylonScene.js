const createScene =  () => {
    const scene = new BABYLON.Scene(engine);
    const camera = new BABYLON.ArcRotateCamera("camera", -Math.PI / 2, Math.PI / 2.5, 3, new BABYLON.Vector3(0, 0, 25));
    camera.attachControl(canvas, true);
    const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0));
	const box = BABYLON.MeshBuilder.CreateBox("box", {});
	
	BABYLON.SceneLoader.ImportMesh("", "http://localhost:8080/", "city obj.obj", scene, function (newMeshes, particleSystems) {
		newMeshes[0].position.x = 0.01;
	});

    return scene;
}

