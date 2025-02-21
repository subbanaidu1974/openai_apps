
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule, FormBuilder } from '@angular/forms';
import { RaceEthnicityComponent } from './raceethnicity.component';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

describe('RaceEthnicityComponent', () => {
  let component: RaceEthnicityComponent;
  let fixture: ComponentFixture<RaceEthnicityComponent>;
  let de: DebugElement;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RaceEthnicityComponent],
      imports: [ReactiveFormsModule],
      providers: [FormBuilder]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RaceEthnicityComponent);
    component = fixture.componentInstance;
    de = fixture.debugElement;
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize the form', () => {
    expect(component.raceEthnicityForm).toBeDefined();
    expect(component.raceEthnicityForm.controls['race'].value).toBeNull();
    expect(component.raceEthnicityForm.controls['ethnicity'].value).toBeNull();
  });

  it('should validate required fields', () => {
    const raceControl = component.raceEthnicityForm.controls['race'];
    const ethnicityControl = component.raceEthnicityForm.controls['ethnicity'];

    raceControl.setValue('');
    ethnicityControl.setValue('');

    expect(raceControl.valid).toBeFalse();
    expect(ethnicityControl.valid).toBeFalse();

    raceControl.setValue('Asian');
    ethnicityControl.setValue('Non-Hispanic');

    expect(raceControl.valid).toBeTrue();
    expect(ethnicityControl.valid).toBeTrue();
  });

  it('should submit the form', () => {
    spyOn(component, 'onSubmit');

    component.raceEthnicityForm.controls['race'].setValue('Black');
    component.raceEthnicityForm.controls['ethnicity'].setValue('Hispanic');
    component.onSubmit();

    expect(component.onSubmit).toHaveBeenCalled();
    expect(component.raceEthnicityForm.valid).toBeTrue();
  });

  it('should display error messages for invalid fields', () => {
    const raceControl = component.raceEthnicityForm.controls['race'];
    const ethnicityControl = component.raceEthnicityForm.controls['ethnicity'];

    raceControl.setValue('');
    ethnicityControl.setValue('');

    fixture.detectChanges();

    const raceError = de.query(By.css('.race-error'));
    const ethnicityError = de.query(By.css('.ethnicity-error'));

    expect(raceError.nativeElement.textContent).toContain('Race is required');
    expect(ethnicityError.nativeElement.textContent).toContain('Ethnicity is required');
  });
});
