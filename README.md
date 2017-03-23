
## Usage 

```
    1. Create scenarioName folder and put a edf file inside.
    2. Run convert script to generate to edf file 
        Eg : to generate the target.csv for first time : convert.py -f .\scenes\test_x\                        -> target.csv in .\scene\test_x\
             to generate the latest.csv for next time  : convert.py -f .\scenes\test_x\ -d .\output\test_x\    -> latest.csv in .\ouput\test_x\
    3. Run compare script
        Eg : pytest --junitxml results.xml compare.py     -> the result : latest.json  in .\report\test_x\ and .\result.xml



$ pytest --junitxml results.xml compare.py

============================= test session starts =============================                 
platform win32 -- Python 2.7.12, pytest-3.0.7, py-1.4.32, pluggy-0.4.0                          
rootdir: D:\work\cortex\apps\EmoTest, inifile:                                                  
collected 13 items                                                                              
                                                                                                
compare.py ..F...F......                                                                        
                                                                                                
================================== FAILURES ===================================                 
_______________ test_deltas[test1-fac_all-0.0-0.0111111111111] ________________                 
                                                                                                
scene = 'test1', group = 'fac_all', delta = 0.0, error = 0.011111111111111112                   
                                                                                                
    @mark.parametrize("scene,group,delta, error", results)                                      
    def test_deltas(scene, group, delta, error) :                                               
      assert delta < 0.01, group +" delta non zero in scene "+scene                             
>     assert error < 0.01, group +" error non zero in scene "+scene                             
E     AssertionError: fac_all error non zero in scene test1                                     
E     assert 0.011111111111111112 < 0.01                                                        
                                                                                                
compare.py:60: AssertionError                                                                   
_______________ test_deltas[test1-fac_upp-0.0-0.0277777777778] ________________                 
                                                                                                
scene = 'test1', group = 'fac_upp', delta = 0.0, error = 0.027777777777777776                   
                                                                                                
    @mark.parametrize("scene,group,delta, error", results)                                      
    def test_deltas(scene, group, delta, error) :                                               
      assert delta < 0.01, group +" delta non zero in scene "+scene                             
>     assert error < 0.01, group +" error non zero in scene "+scene                             
E     AssertionError: fac_upp error non zero in scene test1                                     
E     assert 0.027777777777777776 < 0.01                                                        
                                                                                                
compare.py:60: AssertionError                                                                   
===================== 2 failed, 11 passed in 0.63 seconds =====================                 
```

## Dependencies

- pytest
- numpy
- scipy

## How It works

1. Generate Frobius norms for each expected and detected column group, 
1. Generate Means Square Errors for each column group between expected and actual outcomes
2. Report Test failures if differences are geater than 0.01

## Column Groups

- fac_all : All Facial Expressions
- fac_upp : Upper Facial Expressions
- fac_low : Lower Facial Expressions
- fac_eye : Eye Movementl Expressions
- fac_lid : Eye Lid Expressions
- cog_all : All Cognitive  Metrics 
- cog_int : Interest 
- cog_exc : Excitment Metrics
- cog_eng : Engagment Metrics 
- cog_fru : Frustration Metricss
- cog_pow : All Band Powers

## Structure

```
+ scenes
  + {scenarioName}
    - target.csv  // target emostate output
    - source.edf  // input source files
+ output
  + {scenarioName}
    - latest.csv  // new emostate output)
    - {build}.csv // emostate output from prior builds
+ report
  + {scenarioName}
    - latest.json  // latest Json report
    - {build}.json // Results from Prior builds
- results.xml     // xunit compatible results
```

    



