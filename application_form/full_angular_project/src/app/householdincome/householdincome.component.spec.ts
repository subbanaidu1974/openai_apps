import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule, FormBuilder } from '@angular/forms';
import { HouseholdIncomeComponent } from './householdincome.component';
import { By } from '@angular/platform-browser';

describe('HouseholdIncomeComponent', () => {
  let component: HouseholdIncomeComponent;
  let fixture: ComponentFixture<HouseholdIncomeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HouseholdIncomeComponent],
      imports: [ReactiveFormsModule],
      providers: [FormBuilder]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HouseholdIncomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize the form', () => {
    expect(component.householdIncomeForm).toBeDefined();
    expect(component.householdIncomeForm.controls['income']).toBeDefined();
    expect(component.householdIncomeForm.controls['income'].value).toBeNull();
  });

  it('should make the income control required', () => {
    let incomeControl = component.householdIncomeForm.controls['income'];
    incomeControl.setValue('');
    expect(incomeControl.valid).toBeFalsy();
    expect(incomeControl.errors?.['required']).toBeTruthy();
  });

  it('should submit the form', () => {
    const incomeControl = component.householdIncomeForm.controls['income'];
    incomeControl.setValue(50000);
    expect(component.householdIncomeForm.valid).toBeTruthy();

    // Spy on the submit method
    spyOn(component, 'onSubmit');
    const formElement = fixture.debugElement.query(By.css('form'));
    formElement.triggerEventHandler('ngSubmit', null);
    
    expect(component.onSubmit).toHaveBeenCalled();
  });

  it('should display an error message when the income is invalid', () => {
    const incomeControl = component.householdIncomeForm.controls['income'];
    incomeControl.setValue('');
    fixture.detectChanges();

    const errorMessage = fixture.debugElement.query(By.css('.error-message'));
    expect(errorMessage.nativeElement.textContent).toContain('Income is required');
  });
});

