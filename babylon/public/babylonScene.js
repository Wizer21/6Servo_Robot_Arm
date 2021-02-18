const createScene =  () => {
    const scene = new BABYLON.Scene(engine);
    const camera = new BABYLON.ArcRotateCamera("camera", -Math.PI / 2, Math.PI / 2.5, 3, new BABYLON.Vector3(0, 0, 25));
    camera.attachControl(canvas, true);
    const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0));
    
    // GROUND
    const ground = BABYLON.MeshBuilder.CreateGround("ground", {height: 50, width: 50, subdivisions: 4});
    var backgroundMaterialGround = new BABYLON.BackgroundMaterial("ground", scene);
    backgroundMaterialGround.diffuseTexture = new BABYLON.Texture("http://127.0.0.1:8080/models/grass.jpg", scene);    
    ground.material = backgroundMaterialGround;

	//LOAD .OBJ
	BABYLON.SceneLoader.ImportMesh("", "http://localhost:8080/models/", "arm.obj", scene, function (newMeshes, particleSystems, skeletons) {
        console.log(skeletons.bones)
        var arm = newMeshes[0];
        arm.scaling = new BABYLON.Vector3(4, 4, 4);
        arm.position = new BABYLON.Vector3(4, 4, 4);
	});

	// BOXES
    const box = BABYLON.MeshBuilder.CreateBox("box", {height: 2, width: 2, depth: 2}, scene);
    const box1 = BABYLON.MeshBuilder.CreateBox("box1",{height: 1, width: 2, depth: 1}, scene);

    box1.position = new BABYLON.Vector3(2, 2, 2);
    var backgroundMaterialWood = new BABYLON.BackgroundMaterial("ground", scene);
    backgroundMaterialWood.diffuseTexture = new BABYLON.Texture("http://127.0.0.1:8080/models/wood.jpg", scene);    
    box1.material = backgroundMaterialWood;

    // ANIMATION
    var animation = new BABYLON.Animation("torusEasingAnimation", "position", 30, BABYLON.Animation.ANIMATIONTYPE_VECTOR3, BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE);
    // Save actual box position
    var midPos = box.position.add(new BABYLON.Vector3(-40, 0, 0));
    var lastPos = box.position.add(new BABYLON.Vector3(-80, 0, 0));
    // Create position key list
    var keysBox = [];
    keysBox.push({ frame: 0, value: box.position });
    keysBox.push({ frame: 30, value: midPos });
    keysBox.push({ frame: 60, value: lastPos });
    keysBox.push({ frame: 90, value: midPos });
    keysBox.push({ frame: 120, value: box.position });
    animation.setKeys(keysBox);
    // EASING To make the animation more impressive
    var easingFunction = new BABYLON.CircleEase();
    easingFunction.setEasingMode(BABYLON.EasingFunction.EASINGMODE_EASEINOUT);
    animation.setEasingFunction(easingFunction);
    // ADD ANIMATION
    box.animations.push(animation); 
    //Finally, launch animations on torus, from key 0 to key 120 with loop activated
    scene.beginAnimation(box, 0, 120, true);


    // SKYBOX
    var hdrTexture = new BABYLON.CubeTexture("http://localhost:8080/models/skybox", scene);
    scene.createDefaultSkybox(hdrTexture, true, 10000);
 
    return scene;
}

