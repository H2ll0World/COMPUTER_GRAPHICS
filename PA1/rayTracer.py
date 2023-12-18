#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below1

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image 


class Color:
    #self : class instance 자기자신을 나타내는 키워드
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(np.float64)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma
        self.color=np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(np.uint8)

class Surface:
    def __init__(self, surface_type, shader):
        self.surface_type = surface_type
        self.shader = shader

class Sphere(Surface): #Surface class를 상속받아야지
    def __init__(self, shader, center, radius):
        super().__init__("Sphere", shader)
        self.center = center
        self.radius = radius

    #수정, boolean값이 아닌 해당 t 값을 retrun 해야됨
    # 중점이 원점이고 반지름이 1인 구만 해당
    def intersect(self, d, viewPoint):#(self, 방향벡터, 시각위치)
        a = viewPoint - self.center
        #판별식
        test_val = np.dot(a, d) * np.dot(a, d) - np.dot(a,a) + self.radius * self.radius
        if test_val > 0: #ray가 물체와 만난경우
            return (2, (-np.dot(a,d) - np.sqrt(test_val)), (-np.dot(a,d) + np.sqrt(test_val)))
        elif test_val == 0: #접하는 경우
            return (1,1)
        else: #ray가 물체와 안만난 경우
            return (0,0)
        
class Light:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity= intensity
    
class Shader:
    def __init__(self,name,Type,diffuseColor,specularColor,exponent):
        self.name = name
        self.Type = Type
        self.diffuseColor = diffuseColor
        self.specularColor= specularColor
        self.exponent = exponent

    def Lambertian_shading(self, Sphere, light, pos):
        #normal = np.array([pos[0]-Sphere.center[0], pos[1]-Sphere.center[1], pos[2]-Sphere.center[2]])
        normal = pos - Sphere.center
        normal = normal / np.linalg.norm(normal)
        #light_vec = np.array([light.position[0]-pos[0], light.position[1]-pos[1], light.position[2]-pos[2]])
        light_vec = light.position - pos
        light_vec = light_vec / np.linalg.norm(light_vec)
        return self.diffuseColor * light.intensity * max(0, np.dot(normal, light_vec))

    def Phong_shading(self, Sphere, light, pos, cam):
        normal_vector = np.array([pos[0]-Sphere.center[0], pos[1]-Sphere.center[1], pos[2]-Sphere.center[2]])
        normal_vector = normal_vector / np.linalg.norm(normal_vector)
        to_light = np.array([light.position[0]-pos[0],light.position[1]-pos[1],light.position[2]-pos[2]])
        to_camera= np.array([cam.viewPoint[0] -pos[0],cam.viewPoint[1] -pos[1],cam.viewPoint[2] -pos[2]])
        half_vec = (to_light + to_camera) / np.linalg.norm(to_light + to_camera)
        #print("shading test : ", type(self.exponent))
        return self.specularColor * light.intensity * max(0, np.power(np.dot(half_vec, normal_vector), float(self.exponent)))

    #pos : 계산할 구 위의 점 위치, 
    def Shadow(self, Sphere_list, light, pos):
        #print("Shadow_test_POS : ", pos, " , norm : ",np.linalg.norm(pos))
        direction_vec = light.position - pos
        #print("Shadow : ", direction_vec)
        direction_vec = direction_vec / np.linalg.norm(direction_vec)
        for i in range(len(Sphere_list)):
            shadow_result = Sphere_list[i].intersect(direction_vec, pos)
            if shadow_result[0] == 2:
            #print("test_Shadow : ", shadow_result[1], " *,* ", shadow_result[2])
                if shadow_result[1] > -0.0001:
                    return 1 #visual point와 light사이에 물체가 있음
        return 0 #사이에 물체 x


class Camera:
    def __init__(self, viewPoint, viewDir, projNormal, viewUp, projDistance, viewWidth, viewHeight):
        self.viewPoint = viewPoint
        self.viewDir = viewDir
        self.projNormal = projNormal
        self.viewUp = viewUp
        self.projDistance = projDistance
        self.viewWidth = viewWidth
        self.viewHeight = viewHeight
        
        self.W = self.viewDir/np.linalg.norm(self.viewDir)
        #self.U = np.cross(self.W, self.viewUp)        
        self.U = np.cross(self.viewUp, self.W)

        self.U = self.U /np.linalg.norm(self.U)
        self.V = np.cross(self.W, self.U)
        self.V = self.V /np.linalg.norm(self.V)
    
    #각 픽셀마다 camera의 ray 계산
    def getRay(self, ix, iy, imgSize):
        #pass 
        #print("Camera __init__ : W : ",self.W, " U : ", self.U, " V : ",self.V)
        #print("type : ", type(self.viewWidth))
        #print("imgSize Type : ",type(imgSize[0]))
        #return self.projDistance * self.W  + (self.viewWidth / imgSize[0])*((imgSize[0]/2) - ix)*self.U + (self.viewHeight/imgSize[1])*(imgSize[1]/2-iy)*self.V
        return self.projDistance * self.W  + (self.viewWidth / imgSize[0])*((imgSize[0]/2) - ix)*self.U + (self.viewHeight/imgSize[1])*(imgSize[1]/2-iy)*self.V


def main():

    tree = ET.parse(sys.argv[1]) # xml 인자를 받아서, parsing함 -> ElementTree 객체인 tree를 반환
    root = tree.getroot() # XML 파일의 최상위 노드인 root element return

    # set default values
    viewDir=np.array([0,0,-1]).astype(np.float64) #왜 xml에서 불러오지 않는거?
    viewUp=np.array([0,1,0]).astype(np.float64) #왜 xml에서 불러오지 않는거?
    viewProjNormal=-1*viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
    viewWidth=1.0 #?
    viewHeight=1.0 #?
    projDistance=1.0 #?
    intensity=np.array([1,1,1]).astype(np.float64)  # how bright the light is.
    print(np.cross(viewDir, viewUp)) #cross 는 cross product(외적) 계산

    imgSize=np.array(root.findtext('image').split()).astype(np.int32)

    for c in root.findall('camera'):
        viewPoint=np.array(c.findtext('viewPoint').split()).astype(np.float64)
        viewDir =np.array(c.findtext('viewDir').split()).astype(np.float64)
        projNormal =np.array(c.findtext('projNormal').split()).astype(np.float64)
        viewUp =np.array(c.findtext('viewUp').split()).astype(np.float64)
        if(c.findtext('projDistance')):
            projDistance = float(c.findtext('projDistance'))
        viewWidth =float(c.findtext('viewWidth'))
        viewHeight =float(c.findtext('viewHeight'))
    CAM = Camera(viewPoint,viewDir, projNormal,viewUp,projDistance,viewWidth,viewHeight)

    Shader_list = []
    for c in root.findall('shader'):
        shader_name = c.get('name')
        shader_type = c.get('type')
        diffuseColor=np.array(c.findtext('diffuseColor').split()).astype(np.float64)
        if(c.findtext('specularColor') == None):
            specularColor=np.array([0,0,0])
        else:
            specularColor=np.array(c.findtext('specularColor').split()).astype(np.float64)
        #specularColor=np.array([1,1,0])
        if(c.findtext('exponent') == None):
            exponent = 1
        else:
            exponent = c.findtext('exponent')
        Shader_list.append(Shader(shader_name,shader_type,diffuseColor,specularColor,exponent))
    #code.interact(local=dict(globals(), **locals()))  

    #이거 수정해야함 shader 대신 위에서 정의한 shader_list써야함
    shader = Shader(shader_name,shader_type,diffuseColor,specularColor,exponent)

    
    channels=3 #RGB 이니까 3개인듯...
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:]=0 #위엣 zeros로 초기화 된거 아님?
    
    # replace the code block below! #########################################

    # 사용할 numpy 함수
    # np.dot, np.cos, np.sin, np.cross, np.int32, np.float64, np.array
    # np.zeros, np.arrange, np.sqrt, np.linalg.norm, np.clip

    # 일단 sphere생성
    Surface_list = []
    for c in root.findall('surface'):
        surface_type = c.get('type')
        ref = c.find('shader').get('ref')
        center = np.array(c.findtext('center').split()).astype(np.float64)
        radius = float(c.findtext('radius'))
        Surface_list.append(Sphere(ref, center, radius))

    for c in root.findall('light'):
        position = np.array(c.findtext('position').split()).astype(np.float64)
        intensity = np.array(c.findtext('intensity').split()).astype(np.float64)
    light = Light(position, intensity)
    
    for iy in np.arange(imgSize[0]):
        for ix in np.arange(imgSize[1]):
            ray = CAM.getRay(iy, ix, imgSize) #ray를 구하고 #
            ray = ray / np.linalg.norm(ray)
            
            #4개의 구 중 가장 가까이 있는 것을 찾아야함
            flag = -1
            min = np.array([2.0, 100000.1,100000.1])
            #temp = Surface_list[0].intersect(ray, CAM.viewPoint, 0)
            for i in range(len(Surface_list)):
                temp = Surface_list[i].intersect(ray, CAM.viewPoint)
                if temp[0] == 2:
                    #print("temp[1] : ",temp[1], " temp[2] : ",temp[2])
                    if min[1] > temp[1]:
                        flag = i
                        min[1] = temp[1]
                        min[2] = temp[2]

            #temp = Surface_list[0].intersect(ray, CAM.viewPoint, 0) # t값을 리턴함
            if flag != -1: #intersect가 일어난 경우
                #img[ix][iy]=Color(0,1,1).toUINT8()
                pos_in_sphere = CAM.viewPoint + min[1]*ray
                print("min c : ",min[1])
                
                #맞는 shader를 결정
                idx = -1
                cur_shader = Surface_list[flag].shader
                #print(len(Shader_list))
                for i in range(len(Shader_list)):
                    if Shader_list[i].name == cur_shader:
                        idx = i
                
                Phong = Shader_list[idx].Phong_shading(Surface_list[flag], light, pos_in_sphere, CAM)
                print(Shader_list[idx].name, Shader_list[idx].Type, Shader_list[idx].diffuseColor, Shader_list[idx].exponent)
                print("pos c: ",pos_in_sphere)
                Lambertain = Shader_list[idx].Lambertian_shading(Surface_list[flag], light, pos_in_sphere)
                total_shading =  Lambertain + Phong 
                total_color = total_shading
                #print(total_color)
                total = Color(total_color[0], total_color[1], total_color[2])
                total.gammaCorrect(2.2)
                for i in range(3):
                    if total.color[i] > 1:
                        total.color[i] = 1

                img[ix][iy] = total.toUINT8()
                if shader.Shadow(Surface_list, light,pos_in_sphere) == 1:
                    #pass
                    img[ix][iy] = Color(0,0,0).toUINT8()
            #else:
                #img[ix][iy]=Color(0,0,0).toUINT8()
    
    

    #for i in np.arange(imgSize[0]):
    #    for j in np.arange(imgSize[1]):
            #ray = Ray(viewPoint[0],viewPoint[1],viewPoint[2], )

    #정보를 불러와서 Color class안에 있는 함수를 사용하면 될 듯

    #shading visiual point 의 밝기를 결정하는 알고리즘
    #카메라의 dir, 밝의 위치 등을 고려해서

    #diffuse reflection
    #모든 방향으로 일정하게 반사


    #Lambertian shading
    #visual point의 밝기를 계산 shading이랑 무슨차이
    # diffusion coefficient 존재
    
    # ###
    # shading 계산 
    # visual point 에서 light를 향해 ray를 쐈을 때 물체와 만나면
    # shading이 생김
    # ambient 도 존재 : 가장

    # spectular shading을 쓰는 듯
    
    

    rawimg = Image.fromarray(img, 'RGB')
    rawimg.save('out1.png')
    #rawimg.save(sys.argv[1]+'.png')
    
if __name__=="__main__":
    main()
